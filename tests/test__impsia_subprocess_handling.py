#!/usr/bin/env python3
"""TODO"""

import unittest
from impsia_python_toolbox import impsia_subprocess_handling as process_handler


class TestRunCommandline(unittest.TestCase):
	def test_run_commandline_as_subprocess(self):
		results = process_handler.run_commandline_as_subprocess('echo "gotcha stdout" ')
		stdout_value = results['stdout_value']
		self.assertEqual( stdout_value , 'gotcha stdout', 'stdout-result from subprocess not as expected' )


if __name__ == '__main__':
	unittest.main()
	
