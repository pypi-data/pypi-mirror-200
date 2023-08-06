import codearchiver.core
import codearchiver.subprocess
import datetime
import functools
import hashlib
import itertools
import logging
import os
import shutil
import subprocess
import tempfile


_logger = logging.getLogger(__name__)


class _HashingFileReader:
	'''A tiny wrapper around a file-like object which calculates the hash of the file as it is being read.'''

	def __init__(self, fp, hasher = hashlib.sha1, skipStart = 0, skipEnd = 0):
		self._fp = fp
		self._hasher = hasher()
		self._skipStart = skipStart
		self._skipEnd = skipEnd
		self._buf = b''

	def read(self, n):
		data = self._fp.read(n)
		if self._skipStart > 0:
			# Requires that the first block is bigger than skipStart+skipEnd because it otherwise gets very complicated
			# Yes, this fails if the file is smaller than that, but given what it's used for, that's not an issue.
			if len(data) < self._skipStart + self._skipEnd:
				raise ValueError(f'first read is required to return at least {self._skipStart + self._skipEnd} bytes')
			start = self._skipStart
			self._skipStart = 0
		else:
			start = 0
		bufPlusData = self._buf + data
		if self._skipEnd > 0:
			self._buf = bufPlusData[-self._skipEnd:]
			end = -self._skipEnd
		else:
			end = None
		self._hasher.update(bufPlusData[start:end])
		return data

	def digest(self):
		if self._skipStart > 0 or len(self._buf) != self._skipEnd:
			raise ValueError('data skipping failed')
		return self._hasher.digest()


class GitMetadata(codearchiver.core.Metadata):
	fields = (
		codearchiver.core.MetadataField(key = 'Git version', required = True, repeatable = False),
		codearchiver.core.MetadataField(key = 'Based on bundle', required = False, repeatable = True),
		codearchiver.core.MetadataField(key = 'Ref', required = True, repeatable = True),
		codearchiver.core.MetadataField(key = 'Head', required = True, repeatable = False),
		codearchiver.core.MetadataField(key = 'Root commit', required = True, repeatable = True),
		codearchiver.core.MetadataField(key = 'Object', required = False, repeatable = True),
	)
	version = 0


class Git(codearchiver.core.Module):
	name = 'git'
	MetadataClass = GitMetadata

	@staticmethod
	def matches(inputUrl):
		return inputUrl.url.endswith('.git')

	def __init__(self, *args, extraBranches = {}, **kwargs):
		super().__init__(*args, **kwargs)
		self._extraBranches = extraBranches

	def _find_storage_bundles(self, criteria, checkOids, temporary = False):
		'''Search `self._storage` for bundles or temporary metadata matching `criteria` and containing at least one element of `checkOids`. Yields tuples `(name, objects, oids)`.'''
		searchMethod = self._storage.search_metadata if not temporary else self._storage.search_temporary_metadata
		openMethod = self._storage.open_metadata if not temporary else self._storage.open_temporary_metadata
		matchedBundles = {}  # bundle name → (objects, oids)
		for oldBundle in searchMethod(criteria):
			_logger.info(f'Matching bundle: {oldBundle!r}')
			with openMethod(oldBundle) as fp:
				idx = GitMetadata.deserialise(fp)
			isMatch = False
			oldObjects = set()  # commit and tag lines in this bundle
			oldOids = set()  # commit and tag IDs in this bundle
			for key, value in idx:
				if key != 'Object':
					continue
				oid, otype = value.split(' ', 1)
				oldObjects.add(value)
				oldOids.add(oid)
				if otype not in ('commit', 'tag'):
					continue
				if not isMatch and oid in checkOids:
					isMatch = True
			if isMatch:
				yield (oldBundle, oldObjects, oldOids)

	def process(self):
		with tempfile.TemporaryDirectory(prefix = 'tmp.codearchiver.git.', dir = os.getcwd()) as directory:
			bundle = f'{self._id}_git.bundle'
			if os.path.exists(bundle):
				_logger.fatal(f'{bundle!r} already exists')
				raise FileExistsError(f'{bundle!r} already exists')

			_, gitVersion, _ = codearchiver.subprocess.run_with_log(['git', '--version'])
			if not gitVersion.startswith('git version ') or not gitVersion.endswith('\n') or gitVersion[12:-1].strip('0123456789.') != '':
				raise RuntimeError(f'Unexpected output from `git --version`: {gitVersion!r}')
			gitVersion = gitVersion[12:-1]

			_logger.info(f'Cloning {self._url} into {directory}')
			startTime = datetime.datetime.utcnow()
			codearchiver.subprocess.run_with_log(['git', 'clone', '--verbose', '--progress', '--mirror', self._url, directory], env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0'})

			if self._extraBranches:
				for branch, commit in self._extraBranches.items():
					_logger.info(f'Fetching commit {commit} as {branch}')
					r, _, _ = codearchiver.subprocess.run_with_log(['git', 'fetch', '--verbose', '--progress', 'origin', commit], cwd = directory, check = False)
					if r == 0:
						r2, _, _ = codearchiver.subprocess.run_with_log(['git', 'update-ref', f'refs/codearchiver/{branch}', commit, ''], cwd = directory, check = False)
						if r2 != 0:
							_logger.error(f'Failed to update-ref refs/codearchiver/{branch} to {commit}')
					else:
						_logger.error(f'Failed to fetch {commit}')
				# This leaves over a FETCH_HEAD file, but git-bundle does not care about that, so it can safely be ignored.
			endTime = datetime.datetime.utcnow()

			_logger.info('Collecting repository metadata')
			_, refs, _ = codearchiver.subprocess.run_with_log(['git', 'show-ref'], cwd = directory)
			refs = list(map(str.strip, refs.splitlines()))
			_, rootCommits, _ = codearchiver.subprocess.run_with_log(['git', 'rev-list', '--max-parents=0', '--all'], cwd = directory)
			rootCommits = list(filter(None, rootCommits.splitlines()))
			_, objects, _ = codearchiver.subprocess.run_with_log(['git', 'cat-file', '--batch-check', '--batch-all-objects', '--unordered', '--buffer'], cwd = directory)
			objects = {oid: otype for oid, otype, osize in map(functools.partial(str.split, sep = ' '), objects.splitlines())}
			with open(os.path.join(directory, 'HEAD'), 'r') as fp:
				head = fp.read()
			if not head.startswith('ref: refs/heads/') or not head.endswith('\n'):
				raise RuntimeError(f'Unexpected HEAD content: {head!r}')
			head = head[:-1]  # Remove trailing \n

			metadata = self.create_metadata(bundle, startTime, endTime)
			metadata.append('Git version', gitVersion)
			for line in refs:
				metadata.append('Ref', line)
			metadata.append('Head', head)
			for commitId in rootCommits:
				metadata.append('Root commit', commitId)

			# Check whether there are relevant prior bundles to create an incremental one
			commitsAndTags = {oid for oid, otype in objects.items() if otype in ('commit', 'tag')}
			tmpMetadataDependencies = []  # temporary metadata names this depends on, to be resolved later
			baseOids = set()  # all oids this depends on (including temporary metadata, but only commits and tags from there)
			baseInProgressObjects = set()  # 'oid otype' lines for finding the bundles at the end
			newCommitsAndTags = set()  # oids of commits and tags not covered in previous bundles or existing temporary metadata
			temporaryMetadataName = None
			if self._storage:
				_logger.info('Checking for previous bundles')

				# A note on dependency optimisation: we want the minimal set of previous bundles {B0, …, Bn} that maximises the cover with the current clone S.
				# In other words, in the general case, this is a set cover problem between I = S ∩ (B0 ∪ … ∪ Bn} as the universe and Bi ∩ I as the subsets.
				# Fortunately, solving the actual set cover problem is not necessary.
				# This is because the previous bundles must be disjoint: commit/tag objects are never duplicated. (Trees and blobs might be, but deduplicating those isn't possible.)
				# Therefore, any previous bundle that contains at least one commit or tag object in the current clone must be a dependency.

				# To support parallel archival of related repositories, this uses other processes' temporary metadata from and writes its own to storage.
				# First, obtain all relevant prior bundles.
				# Second, obtain all relevant temporary metadata. Make a note of these and also exclude their commits from this bundle. Write own temporary metadata.
				# Third, upon completion (below), wait for the depended-on temporary metadata to disappear, search for the corresponding bundles, and finalise own metadata.

				with self._storage.lock():
					for oldBundleName, oldObjects, oldOids in self._find_storage_bundles([('Module', type(self).name), ('Root commit', tuple(rootCommits))], commitsAndTags):
						metadata.append('Based on bundle', oldBundleName)
						baseOids |= oldOids
					for tmpMetadataName, tmpObjects, tmpOids in self._find_storage_bundles([('Module', type(self).name), ('Root commit', tuple(rootCommits))], commitsAndTags, temporary = True):
						tmpMetadataDependencies.append(tmpMetadataName)
						baseOids |= tmpOids
						baseInProgressObjects |= tmpObjects

					newCommitsAndTags = commitsAndTags - baseOids
					for oid in newCommitsAndTags:
						metadata.append('Object', f'{oid} {objects[oid]}')
					temporaryMetadataName = self._storage.add_temporary_metadata(metadata)

			try:
				_logger.info(f'Bundling into {bundle}')
				cmd = ['git', 'bundle', 'create', '--progress', f'../{bundle}', '--stdin', '--reflog', '--all']
				objectsToExclude = baseOids & commitsAndTags
				del commitsAndTags
				input = ''.join(f'^{o}\n' for o in objectsToExclude).encode('ascii')
				del objectsToExclude
				status, _, stderr = codearchiver.subprocess.run_with_log(cmd, cwd = directory, input = input, check = False)
				del input
				if status == 128 and (stderr == 'fatal: Refusing to create empty bundle.\n' or stderr.endswith('\nfatal: Refusing to create empty bundle.\n')):
					# Manually write an empty bundle instead
					# Cf. Documentation/technical/bundle-format.txt and Documentation/technical/pack-format.txt in git's repository for details on the formats
					_logger.info('Writing empty bundle directly instead')
					with open(bundle, 'xb') as fp:
						fp.write(b'# v2 git bundle\n')  # bundle signature
						fp.write(b'\n')  # bundle end of prerequisites and refs
						packdata = b'PACK'  # pack signature
						packdata += b'\0\0\0\x02'  # pack version
						packdata += b'\0\0\0\0'  # pack number of objects
						fp.write(packdata)
						fp.write(hashlib.sha1(packdata).digest())  # pack checksum trailer
				elif status != 0:
					raise RuntimeError(f'git bundle creation returned with non-zero exit status {status}.')

				_logger.info('Indexing bundle')

				# The bundle's packfile might contain deltified objects.
				# Those cannot be run through `index-pack` without using `--fix-thin` and running it in a repo containing the missing objects.
				# However, `--fix-thin` has the side effect that it appends those missing objects to the output pack as well, so they also show up in the `show-index` output afterwards.
				# The fact that this always appends is undocumented, so it can't simply be relied on.
				# So this does the following:
				# - Index the pack; as the data is being read, calculate a hash of the pack data without header and trailer checksum
				# - Verify that the corresponding bytes from the index-pack output file have the same hash.
				# - Read the index and filter out any entries that lie beyond the size of the bundle packfile minus 20 (trailer checksum)
				# This gets an accurate index of exactly which objects are in this pack; some might depend on data from other bundles, but that's fine.
				# The extra copy to disk is unfortunately unavoidable anyway, but this hash verification at least makes it somewhat valuable.

				# Index with inline hash calculation
				bundleSize = os.path.getsize(bundle)
				with open(bundle, 'rb') as fpin:
					# Skip over header
					for line in fpin:
						if line == b'\n':
							break
					packOffset = fpin.tell()
					hashWrapper = _HashingFileReader(fpin, skipStart = 12, skipEnd = 20)
					codearchiver.subprocess.run_with_log(['git', 'index-pack', '-v', '--fix-thin', '--stdin', '../tmp.pack'], input = hashWrapper, cwd = directory)
					bundlePackSize = bundleSize - packOffset - 12 - 20
					bundlePackHash = hashWrapper.digest()
				# Verify hash of first part of the index-pack output pack
				with open('tmp.pack', 'rb') as fp:
					fp.seek(12) # Header
					indexPackRead = 0
					hasher = hashlib.sha1()
					while indexPackRead < bundlePackSize:
						data = fp.read(min(bundlePackSize - indexPackRead, 1048576))
						indexPackRead += len(data)
						hasher.update(data)
					indexPackHash = hasher.digest()
				if bundlePackHash != indexPackHash or indexPackRead != bundlePackSize:
					raise RuntimeError(f'index pack hash comparison failed: expected {bundlePackHash!r} (size: {bundlePackSize}), got {indexPackHash!r} (size: {indexPackRead})')
				# Parse index
				with open('tmp.idx', 'rb') as fp:
					_, index, _ = codearchiver.subprocess.run_with_log(['git', 'show-index'], input = fp)
				indexObjectIds = {oid for offset, oid, _ in map(lambda l: l.rstrip('\n').split(' ', 2), index.splitlines()) if int(offset) < bundlePackSize}
				del index
				try:
					indexObjects = {oid: objects[oid] for oid in indexObjectIds}
				except KeyError as e:
					# This should never happen since the bundle is created from the clone with exclusions...
					raise RuntimeError(f'Bundle {bundle} contains object not contained in the present clone') from e
				os.remove('tmp.pack')
				os.remove('tmp.idx')

				_logger.info('Checking for submodules')
				_, commitsWithSubmodules, _ = codearchiver.subprocess.run_with_log(['git', 'log', '--format=format:%H', '--diff-filter=d', '--all', '--', '.gitmodules'], cwd = directory)
				if commitsWithSubmodules:
					_logger.warning('Submodules found but extraction not supported')
				del commitsWithSubmodules

				# Ensure that all commits and tags included in the temporary metadata made it into the pack, else data may be lost!
				indexCommitsAndTags = {oid for oid, otype in indexObjects.items() if otype in ('commit', 'tag')}
				if newCommitsAndTags - indexCommitsAndTags != set():
					raise RuntimeError('Bundle does not contain all commits/tags that were written to temporary metadata, aborting due to data loss risk')
				for oid, otype in indexObjects.items():
					if oid in newCommitsAndTags:
						# Already added to metadata earlier
						continue
					metadata.append('Object', f'{oid} {otype}')
				del indexObjects, indexCommitsAndTags

				# Bundling completed without issues; wait for depended-on bundles, add them to the metadata, then replace own temporary metadata
				if self._storage:
					if tmpMetadataDependencies:
						self._storage.wait_temporary_metadata(tmpMetadataDependencies)
					with self._storage.lock():
						if tmpMetadataDependencies:
							criteria = [('Module', type(self).name), ('Root commit', tuple(rootCommits)), ('Object', tuple(baseInProgressObjects))]
							missingObjects = baseInProgressObjects.copy()
							for oldBundleName, oldObjects, oldOids in self._find_storage_bundles(criteria, {value.split(' ', 1)[0] for value in baseInProgressObjects}):
								metadata.append('Based on bundle', oldBundleName)
								baseOids |= oldOids
								missingObjects -= oldObjects

							# Verification: all commit/tag objects collected from temporary metadata must be covered
							if missingObjects:
								raise RuntimeError('Resolved temporary metadata bundles do not cover all expected objects')

						# Verification: all objects in the clone are either in a base bundle or in the index
						# This can only be done here because all oids are needed, not just the commit/tag objects
						if objects.keys() - (baseOids | indexObjectIds) != set():
							raise RuntimeError('Object mismatch between clone and bundles')

						self._storage.replace_temporary_metadata(temporaryMetadataName, bundle, metadata)
			except:
				# Attempt to remove the temporary metadata, then reraise
				if self._storage:
					with self._storage.lock():
						self._storage.remove_temporary_metadata(temporaryMetadataName)
				raise

		return codearchiver.core.Result(id = self._id, files = [(bundle, metadata)])

	def __repr__(self):
		return f'{type(self).__module__}.{type(self).__name__}({self._inputUrl!r}, extraBranches = {self._extraBranches!r})'
