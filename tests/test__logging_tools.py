#!/usr/bin/env python3
"""Unit test cases for testing the logging tools and logging utilities of sidlogism_python_toolbox."""

from datetime import datetime
from logging import Logger
import inspect
import logging
import logging.config
import os
import sys
import time
import unittest
from sidlogism.python_toolbox import logging_tools


_LOGFILE_ENCODING: str = 'UTF-8'
# configure logger for this script
_LOGCONFIG_ENCODING: str = 'UTF-8'
_LOGCONFIG_RELATIVE_PATH: str = 'src/sidlogism/python_toolbox/logging_default_config.ini'
logging.config.fileConfig(_LOGCONFIG_RELATIVE_PATH, disable_existing_loggers=False, encoding=_LOGCONFIG_ENCODING)
_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.NOTSET)

__all__: list[str] = ['TestLoggingTools']


class TestLoggingTools(unittest.TestCase):
	"""Unit test case for testing the logging configuration and the loging tools and utilities of sidlogism_python_toolbox."""

	def setUp(self) -> None:
		# check precondition for tests: global root loglevel must be at least INFO or below:
		root_loglevel: int = _LOGGER.getEffectiveLevel()
		if root_loglevel > logging.INFO:
			self.fail(f'Global root log level {root_loglevel} is set too high. Set it to {logging.INFO} or below.')

	def _compare_last_logline_with_expected_keywords(self, expected_keywords: str) -> None:
		"""Compare the last line of the test-logfile with the given expected keywords and require both to be equal as unit test condition."""
		expected_keywords_length: int = len(expected_keywords)
		with open(file='./testing_sidlogismtoolbox001.log', mode='rt', encoding=_LOGFILE_ENCODING) as logfile:
			# read all lines until EOF and get last line
			lines: list[str] = logfile.read().splitlines()
			last_line: str = lines[-1]
			# extract relevant part at the end of last line for comparison
			logged_content: str = last_line[-expected_keywords_length:]
			self.assertEqual(expected_keywords, logged_content,
				'The logged output from the created logfile is not as expected because it doesn\'t contain the expected keywords.')

	def test_print_my_logwelcome(self) -> None:
		"""Test logging_tools.print_my_logwelcome."""
		# get starting time of test case representing the starting time of the calling python script or module.
		start_time: datetime = datetime.now()
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
		logging_tools.print_my_logwelcome(executing_script_basename, start_time, sys.argv)
		# check the last line of printed welcome-text
		expected_keywords: str = logging_tools.LOGSEPARATOR_UNDERSCORE
		self._compare_last_logline_with_expected_keywords(expected_keywords)

	def test_print_my_loggoodbye(self) -> None:
		"""Test logging_tools.print_my_loggoodbye."""
		# get starting time of test case representing the starting time of the calling python script or module.
		start_time: datetime = datetime.now()
		# sleep one second so that the computed time delta is not too small
		time.sleep(1)
		logging_tools.print_my_loggoodbye(start_time)
		# check the last line of printed goodbye-text
		expected_keywords: str = logging_tools.LOGSEPARATOR_HASH
		self._compare_last_logline_with_expected_keywords(expected_keywords)

	def test_logging_config(self) -> None:
		"""Test logging-config in general."""
		expected_keywords: str = 'gotcha! logging was successful!'
		_LOGGER.info(expected_keywords)
		# check the last line of printed log-text
		self._compare_last_logline_with_expected_keywords(expected_keywords)

	def test_logging_hierarchy(self) -> None:
		"""Test logging hierarchy via child logger."""
		expected_keywords: str = 'gotcha! logging via child logger was successful!'
		child_logger = _LOGGER.getChild('childlogger')
		child_logger.info(expected_keywords)
		# check the last line of printed log-text
		self._compare_last_logline_with_expected_keywords(expected_keywords)


if __name__ == '__main__':
	unittest.main()
