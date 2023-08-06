import argparse
import contextlib
import datetime
import inspect
import logging
import os
import requests.models
# Imported in parse_args() and main() after setting up the logger:
#import codearchiver.core
#import codearchiver.modules
#import codearchiver.storage
#import codearchiver.version
import tempfile


## Logging
dumpLocals = False
_logger = logging # Replaced below after setting the logger class


class Logger(logging.Logger):
	def _log_with_stack(self, level, *args, **kwargs):
		super().log(level, *args, **kwargs)
		if dumpLocals:
			stack = inspect.stack()
			if len(stack) >= 3:
				name = _dump_stack_and_locals(stack[2:][::-1])
				super().log(level, f'Dumped stack and locals to {name}')

	def warning(self, *args, **kwargs):
		self._log_with_stack(logging.WARNING, *args, **kwargs)

	def error(self, *args, **kwargs):
		self._log_with_stack(logging.ERROR, *args, **kwargs)

	def critical(self, *args, **kwargs):
		self._log_with_stack(logging.CRITICAL, *args, **kwargs)

	def log(self, level, *args, **kwargs):
		if level >= logging.WARNING:
			self._log_with_stack(level, *args, **kwargs)
		else:
			super().log(level, *args, **kwargs)


def _requests_preparedrequest_repr(name, request):
	ret = []
	ret.append(repr(request))
	ret.append(f'\n  {name}.method = {request.method}')
	ret.append(f'\n  {name}.url = {request.url}')
	ret.append(f'\n  {name}.headers = \\')
	for field in request.headers:
		ret.append(f'\n    {field} = {_repr("_", request.headers[field])}')
	if request.body:
		ret.append(f'\n  {name}.body = ')
		ret.append(_repr('_', request.body).replace('\n', '\n  '))
	return ''.join(ret)


def _requests_response_repr(name, response, withHistory = True):
	ret = []
	ret.append(repr(response))
	ret.append(f'\n  {name}.url = {response.url}')
	ret.append(f'\n  {name}.request = ')
	ret.append(_repr('_', response.request).replace('\n', '\n  '))
	if withHistory and response.history:
		ret.append(f'\n  {name}.history = [')
		for previousResponse in response.history:
			ret.append(f'\n    ')
			ret.append(_requests_response_repr('_', previousResponse, withHistory = False).replace('\n', '\n    '))
		ret.append('\n  ]')
	ret.append(f'\n  {name}.status_code = {response.status_code}')
	ret.append(f'\n  {name}.headers = \\')
	for field in response.headers:
		ret.append(f'\n    {field} = {_repr("_", response.headers[field])}')
	ret.append(f'\n  {name}.content = {_repr("_", response.content)}')
	return ''.join(ret)


def _repr(name, value):
	if type(value) is requests.models.Response:
		return _requests_response_repr(name, value)
	if type(value) is requests.models.PreparedRequest:
		return _requests_preparedrequest_repr(name, value)
	valueRepr = repr(value)
	if '\n' in valueRepr:
		return ''.join(['\\\n  ', valueRepr.replace('\n', '\n  ')])
	return valueRepr


@contextlib.contextmanager
def _dump_locals_on_exception():
	try:
		yield
	except Exception as e:
		trace = inspect.trace()
		if len(trace) >= 2:
			name = _dump_stack_and_locals(trace[1:], exc = e)
			_logger.fatal(f'Dumped stack and locals to {name}')
		raise


def _dump_stack_and_locals(trace, exc = None):
	with tempfile.NamedTemporaryFile('w', prefix = 'codearchiver_locals_', delete = False) as fp:
		if exc is not None:
			fp.write('Exception:\n')
			fp.write(f'  {type(exc).__module__}.{type(exc).__name__}: {exc!s}\n')
			fp.write(f'  args: {exc.args!r}\n')
			fp.write('\n')

		fp.write('Stack:\n')
		for frameRecord in trace:
			fp.write(f'  File "{frameRecord.filename}", line {frameRecord.lineno}, in {frameRecord.function}\n')
			for line in frameRecord.code_context:
				fp.write(f'    {line.strip()}\n')
		fp.write('\n')

		for frameRecord in trace:
			module = inspect.getmodule(frameRecord[0])
			if not module.__name__.startswith('codearchiver.') and module.__name__ != 'codearchiver':
				continue
			locals_ = frameRecord[0].f_locals
			fp.write(f'Locals from file "{frameRecord.filename}", line {frameRecord.lineno}, in {frameRecord.function}:\n')
			for variableName in locals_:
				variable = locals_[variableName]
				varRepr = _repr(variableName, variable)
				fp.write(f'  {variableName} {type(variable)} = ')
				fp.write(varRepr.replace('\n', '\n  '))
				fp.write('\n')
			fp.write('\n')
			if 'self' in locals_ and hasattr(locals_['self'], '__dict__'):
				fp.write(f'Object dict:\n')
				fp.write(repr(locals_['self'].__dict__))
				fp.write('\n\n')
		name = fp.name
	return name


def parse_args():
	import codearchiver.version

	parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--version', action = 'version', version = f'codearchiver {codearchiver.version.__version__}')
	parser.add_argument('-v', '--verbose', '--verbosity', dest = 'verbosity', action = 'count', default = 0, help = 'Increase output verbosity')
	parser.add_argument('--dump-locals', dest = 'dumpLocals', action = 'store_true', default = False, help = 'Dump local variables on serious log messages (warnings or higher)')
	# Undocumented option to write one line for each artefact filename produced by this process to FD 3.
	parser.add_argument('--write-artefacts-fd-3', dest = 'writeArtefactsFd3', action = 'store_true', help = argparse.SUPPRESS)
	parser.add_argument('url', help = 'Target URL')
	args = parser.parse_args()
	return args


def setup_logging():
	logging.setLoggerClass(Logger)
	global _logger
	_logger = logging.getLogger(__name__)


def configure_logging(verbosity, dumpLocals_):
	global dumpLocals
	dumpLocals = dumpLocals_

	rootLogger = logging.getLogger()

	# Set level
	if verbosity > 0:
		level = logging.INFO if verbosity == 1 else logging.DEBUG
		rootLogger.setLevel(level)
		for handler in rootLogger.handlers:
			handler.setLevel(level)

	# Create formatter
	formatter = logging.Formatter('{asctime}.{msecs:03.0f}  {levelname}  {name}  {message}', datefmt = '%Y-%m-%d %H:%M:%S', style = '{')

	# Remove existing handlers
	for handler in rootLogger.handlers:
		rootLogger.removeHandler(handler)

	# Add stream handler
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	rootLogger.addHandler(handler)


def main():
	setup_logging()
	args = parse_args()
	configure_logging(args.verbosity, args.dumpLocals)

	import codearchiver.core
	import codearchiver.modules
	import codearchiver.storage
	with _dump_locals_on_exception():
		inputUrl = codearchiver.core.InputURL(args.url)
		if args.writeArtefactsFd3:
			artefactsFd = os.fdopen(3, 'w')
		storage = codearchiver.storage.DirectoryStorage(os.getcwd())
		module = codearchiver.core.get_module_instance(inputUrl, storage = storage)
		with tempfile.TemporaryDirectory(prefix = 'tmp.codearchiver.', dir = os.getcwd()) as td:
			_logger.debug(f'Running in {td}')
			os.chdir(td)
			try:
				result = module.process()
			finally:
				os.chdir('..')
		if args.writeArtefactsFd3:
			_logger.debug('Listing artefacts on FD 3')
			with storage.lock():
				artefacts = storage.list_new_files()
			_logger.debug(f'Artefacts: {artefacts!r}')
			with artefactsFd:
				for filename in artefacts:
					print(filename, file = artefactsFd)

if __name__ == '__main__':
	main()
