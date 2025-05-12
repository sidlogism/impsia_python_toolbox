"""
Provide utilities for handling logging.

Attributes:
	LOGSEPARATOR_HASH (str): Line of hash characters for visual separations of logs or text output.
	LOGSEPARATOR_EQUAL (str): Line of equal characters for visual separations of logs or text output.
	LOGSEPARATOR_ASTERISK (str): Line of asterisk characters for visual separations of logs or text output.
	LOGSEPARATOR_UNDERSCORE (str): Line of underscore characters for visual separations of logs or text output.
	LOGSEPARATOR_HYPHEN (str): Line of hyphen characters for visual separations of logs or text output.
	LOGSEPARATOR_DOT (str): Line of dot characters for visual separations of logs or text output.
	_DATEFORMAT_STARTING_TIME (str): Date format for displaying the starting time of the currently executed python script.

Note:
	This module is not intended for direct execution as a standalone script.
"""

from datetime import datetime, timedelta
from logging import Logger
from typing import Optional
import logging
import os
import sys


if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)

# Lines of special characters for separating log sections visually.
LOGSEPARATOR_HASH: str = 20 * '#'
LOGSEPARATOR_EQUAL: str = 20 * '='
LOGSEPARATOR_ASTERISK: str = 20 * ' * '
LOGSEPARATOR_UNDERSCORE: str = 20 * '_'
LOGSEPARATOR_HYPHEN: str = 20 * '-'
LOGSEPARATOR_DOT: str = 20 * '.'

_DATEFORMAT_STARTING_TIME: str = '%H:%M:%S, %Y-%m-%d %A (%d %B %Y)'

__all__: list[str] = [
	'print_my_logwelcome',
	'print_my_loggoodbye',
	'LOGSEPARATOR_HASH',
	'LOGSEPARATOR_EQUAL',
	'LOGSEPARATOR_ASTERISK',
	'LOGSEPARATOR_UNDERSCORE',
	'LOGSEPARATOR_HYPHEN',
	'LOGSEPARATOR_DOT'
	]


def _get_current_user_name() -> str:
	"""
	Get the current OS username from environment-variables for enriching log output (i. e. giving more details on execution context).

	Returns:
		current OS username from environment-variables
	"""
	if os.name == 'nt':
		if 'USERNAME' not in os.environ:
			return 'unknown'
		return os.environ['USERNAME']
	if os.name == 'posix':
		if 'USER' not in os.environ:
			return 'unknown'
		return os.environ['USER']
	return 'unknown'


def _current_user_has_admin_privileges() -> bool:
	"""
	Determine whether current OS user has admin privileges or is root (for enriching log output i. e. giving more details on execution context).

	Returns:
		True if current user has admin privileges or is root, False otherwise.

	Note:
		The below check for posix-systems (unix/linux) only works with root-login or su.
		Maybe it won't work for sudo oder doas, so maybe we should consult sudoers etc.
		http://stackoverflow.com/questions/2946746/python-checking-if-a-user-has-administrator-privileges
	"""
	if os.name == 'nt':
		try:
			# only windows users with admin privileges can read the C:\windows\temp
			os.listdir(os.sep.join([os.environ.get('SystemRoot', r'C:\windows'), 'temp']))
		except OSError:
			return False
		return True
	if os.name == 'posix':
		return bool(os.geteuid() == 0)
	return False


def print_my_logwelcome(executing_script_basename: str, start_time: datetime, argv: Optional[list[str]] = None) -> None:
	"""
	Print an elaborated first status-message containing detailed information about the calling python script or module.

	Args:
		executing_script_basename (str): The basename of the currently executed python file.
		start_time (datetime): The starting time of the script or module execution.
		argv (list[str], optional): The command line arguments passed to the script or module.
	"""
	logger: Logger = logging.getLogger(__name__)
	logger.setLevel(logging.NOTSET)
	logger.info(LOGSEPARATOR_HASH)
	if argv is None:
		logger.info(f'Starting script "{executing_script_basename}" without any CLI-arguments.')
	else:
		logger.info(f'Starting script "{executing_script_basename}" with arguments "{str(argv[1:])}".')
	logger.info(f'Current user:"{str(_get_current_user_name())}" has administrator/superuser privileges:"{str(_current_user_has_admin_privileges())}".')
	logger.info(f'Starting at: {start_time.strftime(_DATEFORMAT_STARTING_TIME)}.')
	if sys.stdin:
		logger.info(f'sys.stdin.isatty():{str(sys.stdin.isatty())}')
	logger.info(f'sys.stdout.isatty():{str(sys.stdout.isatty())}')
	logger.info(f'sys.stderr.isatty():{str(sys.stderr.isatty())}')
	logger.info(LOGSEPARATOR_UNDERSCORE)


def print_my_loggoodbye(start_time: datetime) -> None:
	"""
	Print an elaborated final last status-message containing detailed information about the calling python script or module.

	Args:
		start_time (datetime): The starting time of the script or module execution.
	"""
	logger: Logger = logging.getLogger(__name__)
	logger.setLevel(logging.NOTSET)
	logger.info(LOGSEPARATOR_UNDERSCORE)
	logger.info(f'Finished script which startet at: {start_time.strftime(_DATEFORMAT_STARTING_TIME)}.')
	time_diff: timedelta = datetime.now() - start_time
	logger.info(f'Full script runtime: {str(time_diff)}')
	logger.info('For details see logfile which is usally located in the same directory as executed script.')
	logger.info(LOGSEPARATOR_HASH)
