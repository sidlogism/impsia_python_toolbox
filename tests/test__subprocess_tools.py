#!/usr/bin/env python3
"""Unit test cases for testing the subprocess tools and subproces sutilities of impsia_python_toolbox."""

import unittest
import logging
import subprocess
from logging import Logger
from typing import Any
from src.impsia.python_toolbox.subprocess_tools import SubprocessRunner    # pylint: disable=import-error
from src.impsia.python_toolbox.subprocess_tools import KEY_SUCCESSFUL_PROCESS, KEY_FAILED_PROCESS, KEY_TIMEOUT_PROCESS  # pylint: disable=import-error
########################################
# The above import statement is fine by most linters except for pylint, which throws the following error:
# E0401: Unable to import 'src.impsia.python_toolbox.subprocess_tools' (import-error)
#
# The following import construct is a possible workaround for pylint--error:
# import sys
# sys.path.append('src/')
# from impsia.python_toolbox.subprocess_tools import SubprocessRunner
#
# But this import-construct raises more problems.
# - it's not supported by mypy (import-not-found)
# - it causes another positioning-error in pylint and flake8 (because of the sys.path.append()-statement):
# pylint C0413: Import "from impsia.p... import SubprocessRunner" should be placed at the top of the module (wrong-import-position)
# flake8 E402 module level import not at top of file
########################################
_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

__all__: list[str] = ['TestSubprocessRunner']


class TestSubprocessRunner(unittest.TestCase):
	"""Test SubprocessRunner-wrapper."""
	def test_run_commandline(self) -> None:
		"""Test SubprocessRunner.run_commandline ."""
		echo_text: str = 'gotcha! echo was successful!'
		runner: SubprocessRunner = SubprocessRunner()
		commandline_args = ['echo', f'"{echo_text}"']
		results: dict[str, Any] = runner.run_commandline(commandline_args, suppress_missing_timeout_warning=False)
		self.assertIsNone(results[KEY_TIMEOUT_PROCESS], 'The executed subprocess ran into a timeout unexpectedly.')
		self.assertIsNone(results[KEY_FAILED_PROCESS], 'The executed subprocess failed unexpectedly.')
		process_data: subprocess.CompletedProcess = results[KEY_SUCCESSFUL_PROCESS]
		self.assertIsNotNone(process_data, 'The executed subprocess yielded output None instead of the expected process-object.')
		self.assertIsInstance(process_data, subprocess.CompletedProcess, 'The executed subprocess didn\'t yield a process-object as expected.')
		stdout_value: str = process_data.stdout
		stdout_value = stdout_value.strip().strip('"')
		self.assertEqual(stdout_value, echo_text,
			'The stdout-result from the executed subprocess is not as expected because it doesn\'t contain the expected keywords.')


if __name__ == '__main__':
	unittest.main()
