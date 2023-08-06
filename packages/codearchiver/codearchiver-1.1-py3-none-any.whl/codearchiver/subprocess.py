import logging
import os
import select
import selectors
import subprocess


_logger = logging.getLogger(__name__)


def run_with_log(args, *, check = True, input = None, **kwargs):
	'''
	Run a command using `subprocess.Popen(args, **kwargs)` and log all its stderr output via `logging`.
	`check` has the same semantics as on `subprocess.run`, i.e. raises an exception if the process exits non-zero.
	`input`, if specified, is a `bytes` or a binary file-like object that is fed to the subprocess via stdin.
	`stdin`, `stdout`, and `stderr` kwargs must not be used.
	Returns a tuple with the process's exit status, its stdout output, and its stderr output.
	'''
	badKwargs = {'stdin', 'stdout', 'stderr'}.intersection(set(kwargs))
	if badKwargs:
		raise ValueError(f'Disallowed kwargs: {", ".join(sorted(badKwargs))}')
	_logger.info(f'Running subprocess: {args!r}')
	if input is not None:
		kwargs['stdin'] = subprocess.PIPE
	p = subprocess.Popen(args, **kwargs, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	sel = selectors.DefaultSelector()
	if input is not None:
		sel.register(p.stdin, selectors.EVENT_WRITE)
	sel.register(p.stdout, selectors.EVENT_READ)
	sel.register(p.stderr, selectors.EVENT_READ)
	stdout = []
	stderr = []
	stderrBuf = b''
	if input is not None:
		inputIsBytes = isinstance(input, bytes)
		if inputIsBytes:
			stdinView = memoryview(input)
			stdinOffset = 0
			stdinLength = len(input)
		PIPE_BUF = getattr(select, 'PIPE_BUF', 512)
	while sel.get_map():
		for key, _ in sel.select():
			if key.fileobj is p.stdin:
				try:
					if inputIsBytes:
						stdinOffset += os.write(key.fd, stdinView[stdinOffset : stdinOffset + PIPE_BUF])
					else:
						d = input.read(PIPE_BUF)
						if not d:
							sel.unregister(key.fileobj)
							key.fileobj.close()
						else:
							os.write(key.fd, d)
				except BrokenPipeError:
					sel.unregister(key.fileobj)
					key.fileobj.close()
				else:
					if inputIsBytes and stdinOffset >= stdinLength:
						sel.unregister(key.fileobj)
						key.fileobj.close()
			else:
				data = key.fileobj.read1()
				if not data:
					sel.unregister(key.fileobj)
					key.fileobj.close()
					continue
				if key.fileobj is p.stderr:
					stderr.append(data)
					stderrBuf += data
					*lines, stderrBuf = stderrBuf.replace(b'\r', b'\n').rsplit(b'\n', 1)
					if not lines:
						continue
					lines = lines[0].decode('utf-8').split('\n')
					for line in lines:
						_logger.info(line)
				else:
					stdout.append(data)
	if stderrBuf:
		_logger.info(stderrBuf.decode('utf-8'))
	p.wait()
	assert p.poll() is not None
	if input is not None and inputIsBytes and stdinOffset < len(input):
		_logger.warning(f'Could not write all input to the stdin pipe (wanted to write {len(input)} bytes, only wrote {stdinOffset})')
	_logger.info(f'Process exited with status {p.returncode}')
	if check and p.returncode != 0:
		raise subprocess.CalledProcessError(returncode = p.returncode, cmd = args)
	return (p.returncode, b''.join(stdout).decode('utf-8'), b''.join(stderr).decode('utf-8'))
