#!/usr/bin/env python3
"""Unit test cases for testing the subprocess tools and subprocess utilities of sidlogism_python_toolbox."""

from logging import Logger
from typing import Any
import logging
import subprocess
import sys
import unittest
from sidlogism.python_toolbox.subprocess_tools import KEY_SUCCESSFUL_PROCESS, KEY_FAILED_PROCESS, KEY_TIMEOUT_PROCESS
from sidlogism.python_toolbox.subprocess_tools import SubprocessRunner

_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.NOTSET)

__all__: list[str] = ['TestSubprocessRunner']


class TestSubprocessRunner(unittest.TestCase):
	"""Test SubprocessRunner-wrapper."""
	def test_run_commandline__echo(self) -> None:
		"""Test SubprocessRunner.run_commandline() with simple echo-command."""
		echo_text: str = 'gotcha! echo was successful!'
		runner: SubprocessRunner = SubprocessRunner()
		commandline_args: list[str] = ['echo', f'"{echo_text}"']
		results: dict[str, Any] = runner.run_commandline(commandline_args, suppress_missing_timeout_warning=False)
		self.assertNotIn(KEY_TIMEOUT_PROCESS, results, 'The executed subprocess ran into a timeout unexpectedly.')
		self.assertNotIn(KEY_FAILED_PROCESS, results, 'The executed subprocess failed unexpectedly.')
		if KEY_SUCCESSFUL_PROCESS not in results:
			self.fail('The executed subprocess didn\'t finish successfully as expected.')
		subprocess_metadata: subprocess.CompletedProcess = results[KEY_SUCCESSFUL_PROCESS]
		self.assertIsNotNone(subprocess_metadata, 'The executed subprocess yielded output None instead of the expected process-object.')
		self.assertIsInstance(subprocess_metadata, subprocess.CompletedProcess, 'The executed subprocess didn\'t yield a process-object as expected.')
		self.assertEqual(subprocess_metadata.returncode, 0, 'The resulting process-object contains unexpected return code.')
		self.assertEqual(subprocess_metadata.args, commandline_args, 'The resulting process-object contains different commandline arguments.')
		stdout_value: str = subprocess_metadata.stdout
		stdout_value = stdout_value.strip().strip('"')
		self.assertEqual(stdout_value, echo_text,
			'The stdout-result from the executed subprocess is not as expected because it doesn\'t contain the expected keywords.')

	def test_run_commandline__timeout(self) -> None:
		"""Test SubprocessRunner.run_commandline() with hanging cat-command and thereby force timeout."""
		runner: SubprocessRunner = SubprocessRunner()
		test_timeout_seconds = 1
		commandline_args: list[str] = ['cat', '-']
		results: dict[str, Any] = runner.run_commandline(commandline_args, timeout=test_timeout_seconds)
		self.assertNotIn(KEY_SUCCESSFUL_PROCESS, results, 'The executed subprocess unexpectedly finished successful without timeout.')
		self.assertNotIn(KEY_FAILED_PROCESS, results, 'The executed subprocess failed unexpectedly.')
		if KEY_TIMEOUT_PROCESS not in results:
			self.fail('The executed subprocess didn\'t run into a timeout as expected.')
		timeout_data: subprocess.TimeoutExpired = results[KEY_TIMEOUT_PROCESS]
		self.assertIsNotNone(timeout_data, 'The executed subprocess yielded output None instead of the expected timeout-object.')
		self.assertIsInstance(timeout_data, subprocess.TimeoutExpired, 'The executed subprocess didn\'t yield a timeout-object as expected.')
		self.assertEqual(timeout_data.timeout, test_timeout_seconds, 'The resulting timeout-object contains different value for timeout duration.')
		self.assertEqual(timeout_data.cmd, commandline_args, 'The resulting timeout-object contains different commandline arguments.')
		_LOGGER.info(f'timeout info: {timeout_data}')

	def test_run_commandline__error(self) -> None:
		"""Test SubprocessRunner.run_commandline() with crashing cat-command and thereby force error."""
		runner: SubprocessRunner = SubprocessRunner()
		commandline_args: list[str] = ['cat', 'nonExistingFileForTest001.txt']
		results: dict[str, Any] = runner.run_commandline(commandline_args, suppress_missing_timeout_warning=True)
		self.assertNotIn(KEY_SUCCESSFUL_PROCESS, results, 'The executed subprocess unexpectedly finished successful without error.')
		self.assertNotIn(KEY_TIMEOUT_PROCESS, results, 'The executed subprocess ran into a timeout unexpectedly.')
		if KEY_FAILED_PROCESS not in results:
			self.fail('The executed subprocess didn\'t run into an error as expected.')
		error_data: subprocess.CalledProcessError = results[KEY_FAILED_PROCESS]
		self.assertIsNotNone(error_data, 'The executed subprocess yielded output None instead of the expected error-object.')
		self.assertIsInstance(error_data, subprocess.CalledProcessError, 'The executed subprocess didn\'t yield a error-object as expected.')
		self.assertEqual(error_data.returncode, 1, 'The resulting error-object contains unexpected return code.')
		self.assertEqual(error_data.cmd, commandline_args, 'The resulting error-object contains different commandline arguments.')
		_LOGGER.info(f'error object: {error_data}')
		_LOGGER.info(f'error return code: {error_data.returncode}; stderr: "{error_data.stderr}"')

	def test_get_pipes_default_encoding_name(self) -> None:
		"""Test SubprocessRunner.get_pipes_default_encoding_name() and test returned encoding by applying it to stdout."""
		runner: SubprocessRunner = SubprocessRunner()
		pipe_encoding: str = runner.get_pipes_default_encoding_name(sys.stdout, last_resort_encoding='UTF-8')
		# check writing to stdout using the determined encoding
		test_text: str = 'Successfully tested stdout encoding.'
		test_text.encode(pipe_encoding, 'backslashreplace')
		try:
			sys.stdout.write(test_text)
		except UnicodeEncodeError:
			self.fail(f'The determined encoding "{pipe_encoding}" for pipes/streams (stdout etc.) and text files handles '
				'causes encoding exception when used with stdout.')


if __name__ == '__main__':
	unittest.main()
