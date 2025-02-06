"""TODO"""
from typing import List, Dict, Any


if __name__ == "__main__":
	print("ERROR: this module is not intended for direct execution as standalone script.")


ERRNO_UNKNOWN = 1


def run_commandline_as_subprocess(commandline: str) -> Dict[str, Any]:
	"""TODO"""
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
