"""TODO"""
from typing import List, Dict, Any


if __name__ == "__main__":
	print("ERROR: this module is not intended for direct execution as standalone script.")


ERRNO_UNKNOWN = 1


class SubprocessRunner:
	def __init__(self):
		self.encoding = 'utf8'


	def run_commandline(self, commandline: str) -> Dict[str, Any]:
		"""Runs given command line as subprocess (and thereby potentially running external applications).
		
		Usage examples:
		>>> runner = SubprocessRunner()
		>>> results = runner.run_commandline('echo "gotcha stdout" ')
		>>> results['stdout_value']
		'gotcha stdout'
		"""
		stdout_value = 'gotcha stdout'
		stderr_value = 'gotcha stderr'
		subprocess_hangs = False

		results = {}
		results['stdout_value'] = stdout_value
		results['stderr_value'] = stderr_value
		returncode = None
		if returncode:
			results['returncode'] = returncode
		else:
			results['returncode'] = ERRNO_UNKNOWN
		results['subprocess_hangs'] = subprocess_hangs
		return results
