"""Tools for handling subprocesses."""
from logging import Logger
from subprocess import TimeoutExpired, CalledProcessError
from typing import Dict, Any, Optional, TextIO
import io
import locale
import logging
import os
import subprocess
import sys


if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)


KEY_SUCCESSFUL_PROCESS = 'p_success'
KEY_TIMEOUT_PROCESS = 'p_timeout'
KEY_FAILED_PROCESS = 'p_fail'
# The os-names are the names used in os.name (which gives kind of a rough os-category)
# _TESTED_OPERATING_SYSTEMS = ['posix', 'nt']
_TESTED_OPERATING_SYSTEMS = ['posix']
_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.NOTSET)

__all__ = ['SubprocessRunner', 'KEY_SUCCESSFUL_PROCESS', 'KEY_FAILED_PROCESS', 'KEY_TIMEOUT_PROCESS']


class SubprocessRunner:
	"""Utility-wrapper for running subprocesses easily and reliably."""

	def __init__(self):
		"""Initialize wrapper for running subprocesses by determining default stream encoding and checking current OS."""
		self.pipe_encoding: str = self.get_pipes_default_encoding_name(sys.stdout, last_resort_encoding='UTF-8')
		if 'cp850' == self.pipe_encoding:
			_LOGGER.warning('Old Windows-encoding "cp850" is being used as your system default for pipes/streams (stdout etc.) and text files handles. '
				'Consider using "UTF-8 mode" by setting environment variable PYTHONUTF8=1 or setting CLI option -Xutf8 (see PEP 540).')
		# check whether current OS-category was explicitly tested before for using this class
		os_was_tested: bool = False
		for os_category in _TESTED_OPERATING_SYSTEMS:
			if os.name == os_category:
				os_was_tested = True
				break
		if not os_was_tested:
			_LOGGER.warning(f'OS-category "{os.name}" was not explicitly tested before for using this class.')

	def get_pipes_default_encoding_name(self, stream: TextIO, last_resort_encoding: str = 'UTF-8') -> str:
		"""
		Try to determine the supported default encoding for pipes/streams by checking different environment configurations and settings.

		See also https://docs.python.org/3/library/os.html#utf8-mode and https://docs.python.org/3/library/sys.html#sys.stdout .
		"""
		if 'PYTHONIOENCODING' in os.environ:
			_LOGGER.debug(f"ignoring environment variable 'PYTHONIOENCODING':{str(os.environ['PYTHONIOENCODING'])}")

		encoding: Optional[str] = ''
		if isinstance(stream, io.TextIOWrapper) and stream.encoding is not None:
			encoding = stream.encoding
			_LOGGER.debug(f'Using stream.encoding:{encoding}')
			return encoding
		if 'PYTHONUTF8' in os.environ and os.environ['PYTHONUTF8'] == 1:
			_LOGGER.debug('environment variable "PYTHONUTF8" is 1 => defaulting to "UTF-8".')
			return 'UTF-8'

		locale.setlocale(locale.LC_ALL, '')
		try:
			encoding = locale.getpreferredencoding(do_setlocale=False)
		except locale.Error:
			pass
		if encoding:
			_LOGGER.debug(f'Using locale.getpreferredencoding(do_setlocale=False):{encoding}')
			return encoding

		try:
			encoding = locale.getlocale()[1]
		except locale.Error:
			pass
		except IndexError:
			pass
		if encoding:
			_LOGGER.debug(f'Using locale.getlocale()[1]:{encoding}')
			return encoding

		try:
			encoding = sys.getfilesystemencoding()
		except OSError:
			pass
		if encoding:
			_LOGGER.debug(f'Using sys.getfilesystemencoding():{encoding}')
			return encoding

		if encoding is None or len(encoding) == 0:
			encoding = last_resort_encoding
			_LOGGER.debug(f'Resorted to last resort encoding {encoding}')
		return encoding

	def run_commandline(
		self,
		commandline_args: list[str],
		timeout: Optional[int] = None,
		suppress_missing_timeout_warning: bool = False
		) -> Dict[str, Any]:
		"""
		Run given command line as subprocess (and thereby potentially running external applications).

		Usage examples:
		>>> runner: SubprocessRunner = SubprocessRunner()
		>>> results: dict[str, Any] = runner.run_commandline(['echo', '"gotcha! echo was successful!"'], suppress_missing_timeout_warning=True)
		>>> process_data: subprocess.CompletedProcess = results[KEY_SUCCESSFUL_PROCESS]
		>>> stdout_value: str = process_data.stdout
		>>> stdout_value = stdout_value.strip().strip('"')
		>>> stdout_value
		'gotcha! echo was successful!'
		"""
		for arg in commandline_args:
			if arg.strip() == '-':
				_LOGGER.warning('One of the given commandline arguments is "-". Reading from STDIN is not supported by this class!')

		if timeout is None and not suppress_missing_timeout_warning:
			_LOGGER.warning(
				'Missing optional timeout-argument. Toolbox-user (programmer) didn\'t provide a timeout for running this new subprocess.'
				'Thus a hanging subprocess cannot be detected and may run eternally.'
				)
		results: dict[str, Any] = {}
		results[KEY_SUCCESSFUL_PROCESS] = None
		results[KEY_TIMEOUT_PROCESS] = None
		results[KEY_FAILED_PROCESS] = None
		try:
			########################################
			# We could use subprocess.popen instead of subprocess.run for a more fine-grained control over streams, timeouts and corner cases.
			# By using subprocess.popen a hanging subprocess or corner cases like 'cat -' could be detected reliably.
			#
			# But for simple scripting use cases doing so would be breaking a butterfly on an wheel.
			# The required additional efforts and complexity are not justified for simple scripting use cases.
			# An corresponding MeticulousSubprocessRunner might be introduced in the future.
			########################################
			process_data: subprocess.CompletedProcess = subprocess.run(
				commandline_args,
				capture_output=True,
				check=True,
				encoding=self.pipe_encoding,
				timeout=timeout
				)
			results[KEY_SUCCESSFUL_PROCESS] = process_data
			return results
		except TimeoutExpired as e:
			results[KEY_TIMEOUT_PROCESS] = e
			return results
		except CalledProcessError as e:
			results[KEY_FAILED_PROCESS] = e
			return results
