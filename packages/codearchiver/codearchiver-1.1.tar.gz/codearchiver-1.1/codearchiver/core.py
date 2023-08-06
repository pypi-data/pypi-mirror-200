import abc
#import codearchiver.modules  # In get_module_class
import codearchiver.storage
import codearchiver.version
import collections
import contextlib
import dataclasses
import datetime
import functools
import logging
import os
import queue
import requests
import time
import typing
import weakref


_logger = logging.getLogger(__name__)


class InputURL:
	'''
	An input URL

	This primarily exists so multiple modules can access the content behind the URL for checks in `Module.matches` without fetching multiple times.
	It also handles the module name prefix in the scheme part of the URL. Note that `InputURL.url` is then the part without the module name.
	'''

	def __init__(self, url: str):
		if 0 < url.find('+') < url.find('://'):
			# '+' and '://' appear in the URL in this order and there is at least one character each before the + as well as between the two
			self._moduleScheme, self._url = url.split('+', 1)
		else:
			self._moduleScheme = None
			self._url = url
		self._response = None

	@property
	def url(self) -> str:
		'''URL without the module scheme prefix (if any)'''
		return self._url

	@property
	def moduleScheme(self) -> typing.Optional[str]:
		'''Module scheme prefix (if one is included, else `None`)'''
		return self._moduleScheme

	@property
	def content(self) -> str:
		'''HTTP response body upon fetching the URL with GET'''
		if self._response is None:
			self._response = HttpClient().get(self.url)
		return self._response.text

	def __repr__(self):
		return f'{type(self).__module__}.{type(self).__name__}({self._url!r})'


@dataclasses.dataclass
class Result:
	'''Container for the result of a module'''

	id: str
	'''A unique ID for this result'''

	files: list[tuple[str, typing.Optional['Metadata']]] = dataclasses.field(default_factory = list)
	'''List of filenames produced by the run, optionally with metadata'''

	submoduleResults: list[tuple['Module', 'Result']] = dataclasses.field(default_factory = list)
	'''List of related submodules and their results'''


class MetadataValidationError(ValueError):
	pass


@dataclasses.dataclass
class MetadataField:
	key: str
	required: bool
	repeatable: bool


class Metadata(list[tuple[str, str]]):
	'''
	Metadata (key-value mapping, possibly with repeated keys) of a file produced by a module

	Fields are inherited. Subclasses meant to be usable should define their own version; the 'Metadata version' field is set by `Module.create_metadata` and collects all declared versions.
	'''

	fields: tuple[MetadataField] = (
		MetadataField('codearchiver version', required = True, repeatable = False),
		MetadataField('Module', required = True, repeatable = False),
		MetadataField('Metadata version', required = True, repeatable = False),
		MetadataField('ID', required = True, repeatable = False),
		MetadataField('Input URL', required = True, repeatable = False),
		MetadataField('Filename', required = True, repeatable = False),
		MetadataField('Retrieval start time', required = True, repeatable = False),
		MetadataField('Retrieval end time', required = True, repeatable = False),
	)
	'''The fields for this metadata collection'''

	version: int = 0
	'''Version, incremented on every backward-incompatible change'''

	_allFieldsCache: typing.Optional[tuple[MetadataField]] = None

	def append(self, *args):
		if len(args) == 1:
			args = args[0]
		return super().append(args)

	# This should be a @classmethod, too, but that's deprecated since Python 3.11.
	@property
	def _allFields(self):
		'''All fields known by this metadata collection, own ones and all from superclasses'''

		if type(self)._allFieldsCache is None:
			fields = []
			for cls in reversed(type(self).mro()):
				fields.extend(getattr(cls, 'fields', []))
			type(self)._allFieldsCache = tuple(fields)
		return type(self)._allFieldsCache

	def validate(self):
		'''Check that all keys and values conform to the specification'''

		keyCounts = collections.Counter(key for key, _ in self)
		keys = set(keyCounts)

		permittedKeys = set(field.key for field in self._allFields)
		unrecognisedKeys = keys - permittedKeys

		requiredKeys = set(field.key for field in self._allFields if field.required)
		missingRequiredKeys = requiredKeys - keys

		repeatableKeys = set(field.key for field in self._allFields if field.repeatable)
		repeatedKeys = set(key for key, count in keyCounts.items() if count > 1)
		repeatedUnrepeatableKeys = repeatedKeys - repeatableKeys

		errors = []
		if unrecognisedKeys:
			errors.append(f'unrecognised key(s): {", ".join(sorted(unrecognisedKeys))}')
		if missingRequiredKeys:
			errors.append(f'missing required key(s): {", ".join(sorted(missingRequiredKeys))}')
		if repeatedUnrepeatableKeys:
			errors.append(f'repeated unrepeatable key(s): {", ".join(sorted(repeatedUnrepeatableKeys))}')
		if errors:
			raise MetadataValidationError('; '.join(errors))

	def matches(self, criteria: list[tuple[str, typing.Union[str, tuple[str]]]]) -> bool:
		'''
		Check whether the criteria match this metadata collection
		Each criterion consists of a key and one or more possible values. A criterion matches if at least one of the specified values is present in the metadata.
		Multiple criteria may use the same key to perform an AND search.
		The metadata is a match if all criteria match.
		'''

		criteria = criteria.copy()
		_logger.debug(f'Searching metadata for {criteria!r}')
		keysOfInterest = set(key for key, _ in criteria)
		for key, value in self:
			if key not in keysOfInterest:
				continue
			_logger.debug(f'Potentially interesting entry: {key!r} = {value!r}')
			matched = []  # Indices to remove from remaining criteria
			for i, (keyCriterion, valueCriterion) in enumerate(criteria):
				if keyCriterion != key:
					continue
				if isinstance(valueCriterion, str) and valueCriterion == value:
					_logger.debug('Str match')
					matched.append(i)
				elif isinstance(valueCriterion, tuple) and value in valueCriterion:
					_logger.debug('Tuple match')
					matched.append(i)
			for i in reversed(matched):
				_logger.debug(f'Matched remaining criterion {i}: {criteria[i]}')
				del criteria[i]
			if not criteria:
				break
		_logger.debug(f'Remaining unmatched criteria: {criteria!r}')
		return not bool(criteria)

	def serialise(self) -> str:
		'''Convert the metadata to a string suitable for e.g. a simple text file storage'''

		self.validate()
		return ''.join(f'{key}: {value}\n' for key, value in self)

	@classmethod
	def deserialise(cls, f: typing.Union[str, bytes, os.PathLike, typing.TextIO], *, validate = True):
		'''Import a serialised metadata from a filename or file-like object'''

		if isinstance(f, (str, bytes, os.PathLike)):
			cm = open(f, 'r')
		else:
			cm = contextlib.nullcontext(f)
		with cm as fp:
			o = cls((key, value[:-1]) for key, value in map(functools.partial(str.split, sep = ': ', maxsplit = 1), fp))
		if validate:
			o.validate()
		return o


class HttpError(Exception):
	'''An HTTP request failed too many times.'''


class HttpClient:
	'''A thin wrapper HTTP client around Requests with exponential backoff retries and a default user agent for all requests.'''

	defaultRetries: int = 3
	'''Default number of retries on errors unless overridden on creating the HttpClient object'''

	defaultUserAgent: str = f'codearchiver/{codearchiver.version.__version__}'
	'''Default user agent unless overridden on instantiation or by overriding via the headers kwarg'''

	def __init__(self, retries: typing.Optional[int] = None, userAgent: typing.Optional[str] = None):
		self._session = requests.Session()
		self._retries = retries if retries else self.defaultRetries
		self._userAgent = userAgent if userAgent else self.defaultUserAgent

	def request(self,
	            method,
	            url,
	            params = None,
	            data = None,
	            headers: typing.Optional[dict[str, str]] = None,
	            timeout: int = 10,
	            responseOkCallback: typing.Optional[typing.Callable[[requests.Response], tuple[bool, typing.Optional[str]]]] = None,
	           ) -> requests.Response:
		'''
		Make an HTTP request

		For the details on `method`, `url`, `params`, and `data`, refer to the Requests documentation on the constructor of `requests.Request`.
		For details on `timeout`, see `requests.adapters.HTTPAdapter.send`.
		`headers` can be used to specify any HTTP headers. Note that this is case-sensitive. To override the user agent, include a value for the `User-Agent` key here.
		`responseOkCallback` can be used to control whether a response is considered acceptable or not. By default, all HTTP responses are considered fine. If specified, this callable must produce a boolean marking whether the response is successful and an error message string. The string is used for logging purposes when the success flag is `False`; it should be `None` if the first return value is `True`.
		'''

		mergedHeaders = {'User-Agent': self._userAgent}
		if headers:
			mergedHeaders.update(headers)
		headers = mergedHeaders
		for attempt in range(self._retries + 1):
			# The request is newly prepared on each retry because of potential cookie updates.
			req = self._session.prepare_request(requests.Request(method, url, params = params, data = data, headers = headers))
			_logger.info(f'Retrieving {req.url}')
			_logger.debug(f'... with headers: {headers!r}')
			if data:
				_logger.debug(f'... with data: {data!r}')
			try:
				r = self._session.send(req, timeout = timeout)
			except requests.exceptions.RequestException as exc:
				if attempt < self._retries:
					retrying = ', retrying'
					level = logging.WARNING
				else:
					retrying = ''
					level = logging.ERROR
				_logger.log(level, f'Error retrieving {req.url}: {exc!r}{retrying}')
			else:
				if responseOkCallback is not None:
					success, msg = responseOkCallback(r)
				else:
					success, msg = (True, None)
				msg = f': {msg}' if msg else ''

				if success:
					_logger.debug(f'{req.url} retrieved successfully{msg}')
					return r
				else:
					if attempt < self._retries:
						retrying = ', retrying'
						level = logging.WARNING
					else:
						retrying = ''
						level = logging.ERROR
					_logger.log(level, f'Error retrieving {req.url}{msg}{retrying}')
			if attempt < self._retries:
				sleepTime = 1.0 * 2**attempt # exponential backoff: sleep 1 second after first attempt, 2 after second, 4 after third, etc.
				_logger.info(f'Waiting {sleepTime:.0f} seconds')
				time.sleep(sleepTime)
		else:
			msg = f'{self._retries + 1} requests to {req.url} failed, giving up.'
			_logger.fatal(msg)
			raise HttpError(msg)
		raise RuntimeError('Reached unreachable code')

	def get(self, *args, **kwargs):
		'''Make a GET request. This is equivalent to calling `.request('GET', ...)`.'''
		return self.request('GET', *args, **kwargs)

	def post(self, *args, **kwargs):
		'''Make a POST request. This is equivalent to calling `.request('POST', ...)`.'''
		return self.request('POST', *args, **kwargs)


class ModuleMeta(abc.ABCMeta):
	'''Metaclass of modules. This is used to keep track of which modules exist and selecting them. It also enforces module name restrictions and prevents name collisions.'''

	__modulesByName: dict[str, typing.Type['Module']] = {}

	def __new__(cls, *args, **kwargs):
		class_ = super().__new__(cls, *args, **kwargs)
		if class_.name is not None:
			if class_.name.strip('abcdefghijklmnopqrstuvwxyz-') != '':
				raise RuntimeError(f'Invalid class name: {class_.name!r}')
			if class_.name in cls.__modulesByName:
				raise RuntimeError(f'Class name collision: {class_.name!r} is already known')
			cls.__modulesByName[class_.name] = weakref.ref(class_)
			_logger.info(f'Found {class_.name!r} module {class_.__module__}.{class_.__name__}')
		else:
			_logger.info(f'Found nameless module {class_.__module__}.{class_.__name__}')
		return class_

	@classmethod
	def get_module_by_name(cls, name: str) -> typing.Optional[typing.Type['Module']]:
		'''Get a module by name if one exists'''

		if classRef := cls.__modulesByName.get(name):
			class_ = classRef()
			if class_ is None:
				_logger.info(f'Module {name!r} is gone, dropping')
				del cls.__modulesByName[name]
			return class_

	@classmethod
	def iter_modules(cls) -> typing.Iterator[typing.Type['Module']]:
		'''Iterate over all known modules'''

		# Housekeeping first: remove dead modules
		for name in list(cls.__modulesByName): # create a copy of the names list so the dict can be modified in the loop
			if cls.__modulesByName[name]() is None:
				_logger.info(f'Module {name!r} is gone, dropping')
				del cls.__modulesByName[name]

		for name, classRef in cls.__modulesByName.items():
			class_ = classRef()
			if class_ is None:
				# Module class no longer exists, skip
				# Even though dead modules are removed above, it's possible that the code consuming this iterator drops/deletes modules.
				continue
			yield class_

	@classmethod
	def drop(cls, module: 'Module'):
		'''
		Remove a module from the list of known modules

		If a Module subclass is destroyed after `del MyModule`, it is also eventually removed from the list. However, as that relies on garbage collection, it should not be depended on and modules should be dropped with this method explicitly.
		'''

		if module.name is not None and module.name in cls.__modulesByName:
			del cls.__modulesByName[module.name]
			_logger.info(f'Module {module.name!r} dropped')

	def __del__(self, *args, **kwargs):
		if self.name is not None and self.name in type(self).__modulesByName:
			_logger.info(f'Module {self.name!r} is being destroyed, dropping')
			del type(self).__modulesByName[self.name]
		# type has no __del__ method, no need to call it.


class Module(metaclass = ModuleMeta):
	'''An abstract base class for a module.'''

	name: typing.Optional[str] = None
	'''The name of the module. Modules without a name are ignored. Names must be unique and may only contain a-z and hyphens.'''

	MetadataClass: typing.Optional[typing.Type[Metadata]] = None
	'''The Metadata class corresponding to this module, if any.'''

	@staticmethod
	def matches(inputUrl: InputURL) -> bool:
		'''Whether or not this module is for handling `inputUrl`.'''
		return False

	def __init__(self, inputUrl: InputURL, storage: typing.Optional[codearchiver.storage.Storage] = None, id_: typing.Optional[str] = None):
		self._inputUrl = inputUrl
		self._url = inputUrl.url
		self._storage = storage
		self._id = id_
		if self._id is None and type(self).name is not None:
			mangledUrl = self._url.replace('/', '_').replace('?', '_').replace('&', '_').replace('#', '_')
			self._id = f'{type(self).name}_{mangledUrl}_{datetime.datetime.utcnow():%Y%m%dT%H%M%SZ}'
		self._httpClient = HttpClient()

	@abc.abstractmethod
	def process(self) -> Result:
		'''Perform the relevant retrieval(s)'''

	def create_metadata(self, filename: str, startTime: datetime.datetime, endTime: datetime.datetime) -> Metadata:
		'''
		Create a basic Metadata instance appropriate for this module

		`startTime` and `endTime` must be in UTC (e.g. `datetime.datetime.utcnow()`). They should reflect the moments just before and after all interaction with the remote system.
		'''

		if type(self).MetadataClass is None or type(self).name is None:
			raise RuntimeError('Module lacks an MetadataClass or a name; cannot create metadata')
		idx = type(self).MetadataClass()
		idx.append('codearchiver version', codearchiver.version.__version__)
		idx.append('Module', type(self).name)
		metadataVersions = []
		for cls in reversed(type(self).MetadataClass.mro()):
			version = cls.__dict__.get('version')
			if version is None:
				continue
			metadataVersions.append(f'{cls.__module__}.{cls.__qualname__}/{version}')
		idx.append('Metadata version', ' '.join(metadataVersions))
		idx.append('ID', self._id)
		idx.append('Input URL', self._url)
		idx.append('Filename', filename)
		idx.append('Retrieval start time', startTime.strftime('%Y-%m-%d %H:%M:%S.%f UTC'))
		idx.append('Retrieval end time', endTime.strftime('%Y-%m-%d %H:%M:%S.%f UTC'))
		return idx

	def __repr__(self):
		return f'{type(self).__module__}.{type(self).__name__}({self._inputUrl!r})'


def get_module_class(inputUrl: InputURL) -> typing.Type[Module]:
	'''Get the Module class most suitable for handling `inputUrl`.'''

	# Ensure that modules are imported
	# This can't be done at the top because the modules need to refer back to the Module class.
	import codearchiver.modules

	# Check if the URL references one of the modules directly
	if inputUrl.moduleScheme:
		if module := ModuleMeta.get_module_by_name(inputUrl.moduleScheme):
			_logger.info(f'Selecting module {module.__module__}.{module.__name__}')
			return module
		else:
			raise RuntimeError(f'No module with name {inputUrl.moduleScheme!r} exists')

	# Check if exactly one of the modules matches
	matches = [class_ for class_ in ModuleMeta.iter_modules() if class_.matches(inputUrl)]
	if len(matches) >= 2:
		_logger.error('Multiple matching modules for input URL')
		_logger.debug(f'Matching modules: {matches!r}')
		raise RuntimeError('Multiple matching modules for input URL')
	if matches:
		_logger.info(f'Selecting module {matches[0].__module__}.{matches[0].__name__}')
		return matches[0]
	raise RuntimeError('No matching modules for input URL')


def get_module_instance(inputUrl: InputURL, **kwargs) -> Module:
	'''Get an instance of the Module class most suitable for handling `inputUrl`.'''
	return get_module_class(inputUrl)(inputUrl, **kwargs)
