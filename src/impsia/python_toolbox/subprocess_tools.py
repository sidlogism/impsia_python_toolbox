"""Tools for handling subprocesses."""
import os
import sys
import subprocess
from subprocess import TimeoutExpired, CalledProcessError
import logging
from logging import Logger
from typing import Dict, Any, Optional


if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)


KEY_SUCCESSFUL_PROCESS = 'p_success'
KEY_TIMEOUT_PROCESS = 'p_timeout'
KEY_FAILED_PROCESS = 'p_fail'
_ENFORCED_STREAM_ENCODING = 'UTF-8'

__all__ = ['SubprocessRunner', 'KEY_SUCCESSFUL_PROCESS', 'KEY_FAILED_PROCESS', 'KEY_TIMEOUT_PROCESS']


class SubprocessRunner:
	"""Utility-wrapper for running subprocesses easily and reliably."""

	def __init__(self):
		"""Initialize internal intance variables of wrapper for running subprocesses."""
		self.encoding = 'utf8'

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
		logger: Logger = logging.getLogger(__name__)
		logger.setLevel(logging.INFO)
		for arg in commandline_args:
			if arg.strip() == '-':
				logger.warning('One of the given commandline arguments is "-". Reading from STDIN is not supported by this class!')

		if timeout is None and not suppress_missing_timeout_warning:
			logger.warning(
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
				encoding=_ENFORCED_STREAM_ENCODING,
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
