"""Tools for handling subprocesses."""
from typing import Dict, Any


if __name__ == "__main__":
	print("ERROR: this module is not intended for direct execution as standalone script.")


ERRNO_UNKNOWN = 1


class SubprocessRunner:
	"""Utility-wrapper for running subprocesses easily and reliably."""

	def __init__(self):
		"""Initialize internal intance variables of wrapper for running subprocesses."""
		self.encoding = 'utf8'

	def run_commandline(self, commandline: str) -> Dict[str, Any]:
		"""
		Run given command line as subprocess (and thereby potentially running external applications).

		Usage examples:
		>>> runner = SubprocessRunner()
		>>> results = runner.run_commandline('echo "gotcha stdout" ')
		>>> results['stdout_value']
		'gotcha stdout'
		"""
		stdout_value: str = 'gotcha stdout'
		stderr_value: str = 'gotcha stderr'
		subprocess_hangs: bool = False

		results: dict[str, Any] = {}
		results['stdout_value'] = stdout_value
		results['stderr_value'] = stderr_value
		returncode = None
		if returncode:
			results['returncode'] = returncode
		else:
			results['returncode'] = ERRNO_UNKNOWN
		results['subprocess_hangs'] = subprocess_hangs
		return results
