#!/usr/bin/env python3
"""TODO"""

import unittest
from typing import Any
from src.impsia.python_toolbox.subprocess_tools import SubprocessRunner    # pylint: disable=import-error
########################################
# The above import statment is fine by most linters except for pylint, which throws the following error:
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
__all__ = ['TestSubprocessRunner']


class TestSubprocessRunner(unittest.TestCase):
	"""Test SubprocessRunner-wrapper."""
	def test_run_commandline(self) -> None:
		"""Test SubprocessRunner.run_coomandline ."""
		echo_text: str = 'gotcha stdout'
		runner: SubprocessRunner = SubprocessRunner()
		results: dict[str, Any] = runner.run_commandline(f'echo "{echo_text}" ')
		stdout_value: str = results['stdout_value']
		self.assertEqual(stdout_value, echo_text, 'The stdout-result from the executed subprocess is not as expected.')


if __name__ == '__main__':
	unittest.main()
