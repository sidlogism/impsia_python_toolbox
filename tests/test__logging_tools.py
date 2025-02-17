#!/usr/bin/env python3
"""Unit test cases for testing the logging tools and logging utilities of impsia_python_toolbox."""

import unittest
import sys
import os
import inspect
import logging
import logging.config
from logging import Logger
from datetime import datetime
from src.impsia.python_toolbox import logging_tools    # pylint: disable=import-error
########################################
# The above import statement is fine by most linters except for pylint, which throws the following error:
# E0401: Unable to import 'src.impsia.python_toolbox' (import-error)
#
# For more details and possible workarounds see test__subprocess_tools.py.
########################################

LOGFILE_ENCODING: str = 'UTF-8'
# configure logger for this script
LOGCONFIG_ENCODING: str = 'UTF-8'
LOGCONFIG_RELATIVE_PATH: str = 'src/impsia/python_toolbox/logging_default_config.ini'
logging.config.fileConfig(LOGCONFIG_RELATIVE_PATH, disable_existing_loggers=True, encoding=LOGCONFIG_ENCODING)
LOGGER: Logger = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

__all__: list[str] = ['TestLoggingTools']


class TestLoggingTools(unittest.TestCase):
	"""Unit test case for testing the logging configuration and the loging tools and utilities of impsia_python_toolbox."""

	def setUp(self) -> None:
		# get script starting time for logwelcome/loggoodbye
		self.start_time: datetime = datetime.now()

	def _compare_last_logline_with_expected_keywords(self, expected_keywords: str) -> None:
		"""Compare the last line of the test-logfile with the given expected keywords and require both to be equal as unit test condition."""
		expected_keywords_length: int = len(expected_keywords)
		with open(file='./testing_impisatoolbox001.log', mode='rt', encoding=LOGFILE_ENCODING, newline=None) as logfile:
			lines: list[str] = logfile.read().splitlines()
			last_line: str = lines[-1]
			logged_content: str = last_line[-expected_keywords_length:]
			self.assertEqual(expected_keywords, logged_content,
				'The logged output from the created logfile is not as expected because it doesn\'t contain the expected keywords.')

	def test_print_my_logwelcome(self) -> None:
		"""Test logging_tools.print_my_logwelcome."""
		# Get basename of the currenlty executed script file. Don't pass sys.argv[0], but use inspect instead.
		executing_script_basename: str = os.path.basename(inspect.getfile(inspect.currentframe()))    # type: ignore[arg-type]
		########################################
		# The above code line is fine by most linters except for mypy, which throws the following error:
		# error: Argument 1 to "getfile" has incompatible type "FrameType | None"; expected Module | type[Any] | MethodType | FunctionType ...  [arg-type]
		# The above inline comment "# type: ignore[arg-type]" disables this mypy-check on this particular code line.
		#
		# There might by a possible workaround with the cast-function but so far we couldn't find a solution yet.
		# Details on the cast-function from typing module: https://peps.python.org/pep-0484/#casts
		########################################

		# perform the actual logging-test
		logging_tools.print_my_logwelcome(executing_script_basename, sys.argv, self.start_time)
		# check the last line of printed welcome-text
		expected_keywords: str = logging_tools.LOGSEPARATOR_UNDERSCORE
		self._compare_last_logline_with_expected_keywords(expected_keywords)

	def test_print_my_loggoodbye(self) -> None:
		"""Test logging_tools.print_my_loggoodbye."""
		logging_tools.print_my_loggoodbye(self.start_time)
		# check the last line of printed goodbye-text
		expected_keywords: str = logging_tools.LOGSEPARATOR_HASH
		self._compare_last_logline_with_expected_keywords(expected_keywords)

	def test_logging_config(self) -> None:
		"""Test logging-config in general."""
		expected_keywords: str = 'gotcha! logging was successful!'
		LOGGER.info(expected_keywords)
		# check the last line of printed log-text
		self._compare_last_logline_with_expected_keywords(expected_keywords)

	def test_logging_hierarchy(self) -> None:
		"""Test logging hierarchy via child logger."""
		expected_keywords: str = 'gotcha! logging via child logger was successful!'
		child_logger = LOGGER.getChild('childlogger')
		child_logger.info(expected_keywords)
		# check the last line of printed log-text
		self._compare_last_logline_with_expected_keywords(expected_keywords)


if __name__ == '__main__':
	unittest.main()
