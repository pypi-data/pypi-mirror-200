import abc
import codearchiver.core
import collections.abc
import contextlib
import filelock
import glob
import hashlib
import logging
import os
import os.path
import shutil
import time
import typing


_logger = logging.getLogger(__name__)


class Storage(abc.ABC):
	'''
	Interface for storage backing the codearchiver collection
	This serves primarily to aid deduplication by locating prior archives of the same or closely related repositories.
	Filenames must not contain LF.
	'''

	@abc.abstractmethod
	@contextlib.contextmanager
	def lock(self, blocking = True) -> typing.Iterator[bool]:
		'''
		Acquire a lock on the storage.
		If `blocking`, this method blocks until the lock can be acquired.
		Yields whether the lock was acquired. If `blocking`, this is always `True`.
		Once the context manager is exited, the lock shall be released.
		Other methods must only be called while holding the lock unless noted otherwise. The `Storage` class may or may not enforce this.
		'''

	@abc.abstractmethod
	def put(self, filename: str, metadata: typing.Optional['codearchiver.core.Metadata'] = None):
		'''Put a local file and (if provided) its metadata into storage. If an error occurs, a partial copy may remain in storage. If it completes, the local input file is removed.'''

	def put_result(self, result: 'codearchiver.core.Result'):
		'''Put a module's Result into storage. The semantics are as for `put`, and the exact behaviour regarding partial copies and leftover files on errors is undefined.'''
		for fn, metadata in result.files:
			self.put(fn, metadata)
		for _, subresult in result.submoduleResults:
			self.put_result(subresult)

	@abc.abstractmethod
	def list_new_files(self) -> list[str]:
		'''
		List of all files that have been `.put()` on this instance.
		This may include additional files for storing metadata.
		'''
		# The return value must be a copy of the state.

	@abc.abstractmethod
	def search_metadata(self, criteria: list[tuple[str, typing.Union[str, tuple[str]]]]) -> collections.abc.Iterator[str]:
		'''
		Search all metadata in storage by criteria.
		Refer to `codearchiver.core.Metadata.matches` for the semantics of `criteria`.
		Yields all filenames where all criteria match in lexicographical order.
		'''

	@abc.abstractmethod
	@contextlib.contextmanager
	def open_metadata(self, filename: str) -> typing.TextIO:
		'''Open the metadata for a file in serialised form.'''

	@abc.abstractmethod
	@contextlib.contextmanager
	def open(self, filename: str, mode: typing.Optional[str] = 'rb') -> typing.Iterator[typing.Union[typing.BinaryIO, typing.TextIO]]:
		'''Open a file from storage. The mode must be r or rb.'''

	@abc.abstractmethod
	def add_temporary_metadata(self, metadata: 'codearchiver.core.Metadata') -> str:
		'''
		Add a temporary metadata record, to be replaced by permanent data or removed depending on the further processing.
		This is intended to allow for parallel deduplication.
		Every call to this method MUST be paired with a call to either `replace_temporary_metadata` or `remove_temporary_metadata`.
		Returns a unique name for this temporary record for use in the other `*_temporary_metadata` methods.
		'''
		# The name must be unique in perpetuity, i.e. it must never be reused.

	@abc.abstractmethod
	def search_temporary_metadata(self, criteria: list[tuple[str, typing.Union[str, tuple[str]]]]) -> collections.abc.Iterator[str]:
		'''Same as `search_metadata`, but for the temporary metadata written by `add_temporary_metadata`, returning the unique names instead.'''

	@abc.abstractmethod
	def open_temporary_metadata(self, name: str) -> typing.TextIO:
		'''Open temporary metadata.'''

	@abc.abstractmethod
	def replace_temporary_metadata(self, name: str, filename: str, metadata: 'codearchiver.core.Metadata'):
		'''Replace the temporary metadata with a matching proper file and accompanying metadata.'''

	@abc.abstractmethod
	def remove_temporary_metadata(self, name: str):
		'''Remove the temporary metadata without adding a matching proper file instead, e.g. in case of an error.'''

	@abc.abstractmethod
	def wait_temporary_metadata(self, names: list[str], sleepTime: typing.Optional[float] = None):
		'''
		Block until all temporary metadata in `names` are gone.
		`sleepTime` is the time to wait between attempts to check for existence, used for storage layers that do not support direct monitoring.
		The caller should afterwards use `search_metadata` with appropriate `criteria` to find matching permanent files.
		This method must be called without holding the global storage lock.
		'''


class DirectoryStorage(Storage):
	def __init__(self, directory):
		super().__init__()
		self._directory = directory
		self._newFiles = []
		self._lock = filelock.FileLock(os.path.join(self._directory, '.lock'))

	@contextlib.contextmanager
	def lock(self, blocking = True):
		try:
			with self._lock.acquire(blocking = blocking):
				yield True
		except filelock.Timeout:
			yield False

	def _check_directory(self):
		exists = os.path.exists(self._directory)
		if exists and not os.path.isdir(self._directory):
			raise NotADirectoryError(self._directory)
		return exists

	def _ensure_directory(self):
		if not self._check_directory():
			os.makedirs(self._directory)

	def put(self, filename, metadata = None):
		self._ensure_directory()
		if '\n' in filename:
			raise ValueError(fr'filenames cannot contain \n: {filename!r}')
		#FIXME: Race condition
		if os.path.exists((targetFilename := os.path.join(self._directory, os.path.basename(filename)))):
			raise FileExistsError(f'{targetFilename} already exists')
		_logger.info(f'Moving {filename} to {self._directory}')
		shutil.move(filename, self._directory)
		self._newFiles.append(filename)
		if not metadata:
			return
		metadataFilename = f'{filename}_codearchiver_metadata.txt'
		metadataPath = os.path.join(self._directory, metadataFilename)
		# No need to check for existence here thanks to the 'x' mode
		_logger.info(f'Writing metadata for {filename} to {metadataFilename}')
		with open(metadataPath, 'x') as fp:
			fp.write(metadata.serialise())
		self._newFiles.append(metadataFilename)

	def list_new_files(self):
		return self._newFiles.copy()

	def search_metadata(self, criteria, _suffix = '_codearchiver_metadata.txt'):
		_logger.info(f'Searching metadata by criteria: {criteria!r}')
		# Replace this with `root_dir` when dropping Python 3.9 support
		prefix = os.path.join(self._directory, '')
		escapedDirPrefix = glob.escape(prefix)
		escapedSuffix = glob.escape(_suffix)
		files = glob.glob(f'{escapedDirPrefix}*{escapedSuffix}')
		files.sort()
		for metadataFilename in files:
			metadataFilename = metadataFilename[len(prefix):]
			assert '\n' not in metadataFilename
			_logger.info(f'Searching metadata {metadataFilename}')
			with self.open(metadataFilename, 'r') as fp:
				idx = codearchiver.core.Metadata.deserialise(fp, validate = False)
			if idx.matches(criteria):
				_logger.info(f'Found metadata match {metadataFilename}')
				yield metadataFilename[:-len(_suffix)]
		_logger.info('Done searching metadata')

	@contextlib.contextmanager
	def open_metadata(self, filename):
		with self.open(f'{filename}_codearchiver_metadata.txt', 'r') as fp:
			yield fp

	@contextlib.contextmanager
	def open(self, filename, mode = 'rb'):
		if '\n' in filename:
			raise ValueError(fr'filenames cannot contain \n: {filename!r}')
		with open(os.path.join(self._directory, filename), mode) as fp:
			yield fp

	def add_temporary_metadata(self, metadata):
		# Build a filename based on the current time in nanoseconds and a (truncated) hash of the metadata; this should guaranteed uniqueness to a sufficient degree.
		serialised = metadata.serialise().encode('utf-8')
		metadataHash = hashlib.sha512(serialised).hexdigest()[:128]
		name = f'tmp_{time.time_ns()}_{metadataHash}'
		filename = f'{name}_codearchiver_temporary_metadata.txt'
		self._ensure_directory()
		_logger.info(f'Writing temporary metadata to {filename}')
		with open(os.path.join(self._directory, filename), 'xb') as fp:
			fp.write(serialised)
		_logger.info('Done writing temporary metadata file')
		return name

	def search_temporary_metadata(self, criteria):
		yield from self.search_metadata(criteria, _suffix = '_codearchiver_temporary_metadata.txt')

	@contextlib.contextmanager
	def open_temporary_metadata(self, name):
		with self.open(f'{name}_codearchiver_temporary_metadata.txt', 'r') as fp:
			yield fp

	def replace_temporary_metadata(self, name, filename, metadata):
		_logger.info(f'Replacing temporary metadata file {name}')
		self.put(filename, metadata)
		self.remove_temporary_metadata(name)

	def remove_temporary_metadata(self, name):
		if name.endswith('_codearchiver_temporary_metadata.txt'):
			raise RuntimeError('invalid temporary metadata name provided')
		_logger.info(f'Removing temporary metadata file {name}')
		os.remove(os.path.join(self._directory, f'{name}_codearchiver_temporary_metadata.txt'))

	def wait_temporary_metadata(self, names, sleepTime = 5):
		_logger.info(f'Waiting for temporary metadata: {names!r}')
		remaining = {os.path.join(self._directory, f'{name}_codearchiver_temporary_metadata.txt') for name in names}
		while remaining:
			with self.lock(blocking = False) as locked:
				if locked:
					remaining = {filename for filename in remaining if os.path.exists(filename)}
					_logger.debug(f'Remaining: {remaining!r}')
			if not remaining:
				break
			time.sleep(sleepTime)
		_logger.info('All temporary metadata files gone')
