"""
Miscellaneous shared components and tools used by the other modules in sidlogism_python_toolbox.

This module provides common utility functions and error classes used across different
problem domains. It includes tools for file path handling, string sanitization, and
custom error types.

Attributes:
	ERRNO_SUCCESS (int): Success error code (default 0 on Unix-like systems, may vary depending on the OS)
	ERRNO_USAGE (int): Usage error code (default 2 on Unix-like systems, may vary depending on the OS)
	ERRNO_UNKNOWN (int): Unknown error code (default 1 on Unix-like systems, may vary depending on the OS)
	_LOGGER (Logger): Module-level logger instance

Note:
	This module is not intended for direct execution as a standalone script.
"""
from logging import Logger
import logging
import os
import re
import sys

if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)


ERRNO_SUCCESS: int = 0
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_SUCCESS = os.EX_OK
except AttributeError:
	pass

ERRNO_USAGE: int = 2
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_USAGE = os.EX_USAGE
except AttributeError:
	pass

ERRNO_UNKNOWN: int = 1
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_UNKNOWN = os.EX_SOFTWARE
except AttributeError:
	pass

_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.NOTSET)

__all__: list[str] = ['ERRNO_SUCCESS', 'ERRNO_USAGE', 'ERRNO_UNKNOWN', 'SidlogismError', 'UsageError',
	'strip_fileextension', 'sanitize_input_string', 'sanitize_userinput_path']


class SidlogismError(Exception):
	"""
	Generic exception base class for customized exception types for sidlogism_python_toolbox-specific errors.

	Attributes:
		errno (int): Error number, defaults to ERRNO_UNKNOWN
		msg (str): Error message describing the issue
	"""

	errno: int = ERRNO_UNKNOWN
	msg: str

	def __init__(self, msg):
		"""
		Initialize SidlogismError object with a message.

		Args:
			msg (str): Description of the error
		"""
		self.msg = msg

	def __str__(self) -> str:
		"""
		Paraphrase SidlogismError object as string: Convert error to string representation.

		Returns:
			string representation of the error
		"""
		return self.msg


class UsageError(SidlogismError):
	"""
	Customized exception for incorrect usage of sidlogism_python_toolbox functionality.

	This exception is raised when functions or methods are used incorrectly,
	such as providing invalid parameters or violating usage constraints.

	Attributes:
		errno (int): Error number, defaults to 2 or os.EX_USAGE if available
	"""

	errno = ERRNO_USAGE

	def __init__(self, msg):
		"""
		Initialize UsageError object with a message.

		Args:
			msg (str): Description of the usage error
		"""
		super().__init__(msg)
		try:
			# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
			type(self).errno = os.EX_USAGE
		except AttributeError:
			pass


def strip_fileextension(file_basename: str) -> str:
	"""
	Remove the file extension from a filename.

	Args:
		file_basename (str): The filename to process

	Returns:
		Filename with the extension removed

	Raises:
		UsageError: If file_basename contains path separators
	"""
	if file_basename.startswith('./') or file_basename.startswith(os.curdir + os.sep):
		# strip leading './'
		file_basename = file_basename[2:]
	if os.sep in file_basename:
		raise UsageError(f'The given file base name "{file_basename}" is invalid because it seems to contain some path fragments. '
			'It contains the directory separator symbol "{os.sep}" for separating directories within filesystem paths.')
	stripped_basename: str = os.path.splitext(os.path.basename(file_basename))[0]
	return stripped_basename


def sanitize_input_string(user_string: str, encoding: str, whitelist: str, blacklist: str) -> None:
	"""
	Sanitize and validate given user input string against allowed/disallowed characters and encoding by throwing exception.

	Args:
		user_string (str): The string to validate
		encoding (str): The required string encoding (e.g., 'utf-8')
		whitelist (str): Regular expression pattern of allowed characters
		blacklist (str): Regular expression pattern of disallowed characters

	Raises:
		UnicodeEncodeError: If string contains characters not supported by the encoding
		UsageError: If string contains characters matching blacklist or not matching whitelist
	"""
	user_string.encode(encoding, errors='strict')
	patterns: list[str] = []
	if blacklist:
		blacklist = r'[' + blacklist + r']+'
		patterns.append(blacklist)
	if whitelist:
		whitelist = r'[^' + whitelist + r']+'
		patterns.append(whitelist)
	for pattern in patterns:
		# aborting with error message (blocking) as soon as an invalid character was found.
		regex: re.Pattern = re.compile(pattern, re.UNICODE)
		if regex.search(user_string) is not None:
			raise UsageError(f'Argument "{user_string}" contains invalid chars :"{str(regex.findall(user_string))}" (pattern:"{pattern}")')


def sanitize_userinput_path(path: str, encoding: str,  # pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
							mustbe_file: bool = False, maybe_file: bool = False,
							mustbe_directory: bool = False, maybe_directory: bool = False,
							mustbe_symlink: bool = False, maybe_symlink: bool = False,
							mustbe_readable: bool = False, maybe_readable: bool = False,
							mustbe_writable: bool = False, maybe_writable: bool = False,
							mustbe_executable: bool = False, maybe_executable: bool = False) -> str:
	"""
	Sanitize and validate given path from user input.

	This function performs comprehensive validation of a filesystem path, checking its existence and attributes.
	It also sanitizes the path string against potentially harmful characters.

	Args:
		path (str): The filesystem path to validate
		encoding (str): The required string encoding for the path
		mustbe_file (bool, optional): Path must be a regular file. Defaults to False
		maybe_file (bool, optional): Path is allowed to be a regular file. Defaults to False
		mustbe_directory (bool, optional): Path must be a directory. Defaults to False
		maybe_directory (bool, optional): Path is allowed to be a directory. Defaults to False
		mustbe_symlink (bool, optional): Path must be a symbolic link. Defaults to False
		maybe_symlink (bool, optional): Path is allowed to be a symbolic link. Defaults to False
		mustbe_readable (bool, optional): Path must be readable. Defaults to False
		maybe_readable (bool, optional): Path is allowed to be readable. Defaults to False
		mustbe_writable (bool, optional): Path must be writable. Defaults to False
		maybe_writable (bool, optional): Path is allowed to be writable. Defaults to False
		mustbe_executable (bool, optional): Path must be executable. Defaults to False
		maybe_executable (bool, optional): Path is allowed to be executable. Defaults to False

	Returns:
		The validated and sanitized path (absolute path)

	Raises:
		UsageError: If path validation fails or if function parameters are inconsistent

	Note:
		- The function only considers symlinks, directories, and regular files
		- Path expansion for special directory names (e. g. "~") is not supported yet
		- The function does not check for FIFOs, sockets, or other special file types
		- Mind the "mustbe"-flags and "maybe"-flags! Per default they are all set to False, which simply disqualifies all paths!
		- At least one of maybe_symlink, maybe_directory, or maybe_file must be True (according to your use case)
		- If a 'mustbe_*' flag is True, the corresponding 'maybe_*' flag is automatically set to True
		- Special handling is implemented for Windows drive letters
	"""
	########################################
	# Check that flag logic is correctly used and infer correct values of "maybe"-flags:
	# If a "mustbe"-flag is True, the corresponding "maybe"-flag will be automatically set to True.
	########################################
	if mustbe_file:
		maybe_file = True
		if mustbe_symlink or mustbe_directory:
			raise UsageError(
				'Wrong parametrization of function. '
				'The item identified by a path can only be enforced to be one single category at a time out of the following three categories: '
				'symlink or directory or file.')
	if mustbe_directory:
		maybe_directory = True
		if mustbe_symlink or mustbe_file:
			raise UsageError(
				'Wrong parametrization of function. '
				'The item identified by a path can only be enforced to be one single category at a time out of the following three categories: '
				'symlink or directory or file.')
	if mustbe_symlink:
		maybe_symlink = True
		if mustbe_directory or mustbe_file:
			raise UsageError(
				'Wrong parametrization of function. '
				'The item identified by a path can only be enforced to be one single category at a time out of the following three categories: '
				'symlink or directory or file.')
	if mustbe_readable:
		maybe_readable = True
	if mustbe_writable:
		maybe_writable = True
	if mustbe_executable:
		maybe_executable = True
	# safety check in hindsight:
	#     "mustbe"-flag A is True => corresponding "maybe"-flag B must be True
	#     mustbe_X => maybe_X
	#     if A is true, B MUST be true
	# The boolean statement (A => B) is equal to (not A or B):
	assert (not mustbe_file or maybe_file)
	assert (not mustbe_directory or maybe_directory)
	assert (not mustbe_symlink or maybe_symlink)
	assert (not mustbe_readable or maybe_readable)
	assert (not mustbe_writable or maybe_writable)
	assert (not mustbe_executable or maybe_executable)
	if not maybe_symlink and not maybe_directory and not maybe_file:
		raise UsageError('Wrong parametrization of function. Path must be allowed to be at least one category out of symlinks, directories or files.')

	whitelist: str = r'\w'  # UNICODE word characters (see python doc of module "re").
	whitelist += r'\. \-_'  # valid components of directory names of filenames (space too, though deprecated , but NOT other whitespace !!)
	if os.extsep:
		whitelist += str(os.extsep)
	whitelist += r'/\\'  # directory separators
	if os.sep:
		whitelist += str(os.sep)
	if os.altsep:
		whitelist += str(os.altsep)
	whitelist += r'~'  # valid wildcards
	whitelist += r':'  # special path components

	blacklist: str = r';&'  # command separators
	blacklist += r'\'"'  # single and double quotes
	blacklist += r'#!'  # shell-script comment indicators
	blacklist += r'\$%'  # shell-variable indicators
	blacklist += r'\r\n'  # newlines
	if os.linesep:
		blacklist += str(os.linesep)

	sanitize_input_string(path, encoding, whitelist, blacklist)

	########################################
	# check if path exists
	#
	# Details on os.path.exists(path):
	# On some platforms, this function may return False if permission is not granted to execute os.stat() on the requested file,
	# even if the path physically exists.
	########################################
	# if not os.access(path, os.F_OK):
	errormsg = ' => your argument in the following line is invalid:\n' + path
	if not os.path.exists(path):
		raise UsageError("Path doesn't exist or is not readable or doesn't grant permissions for os.stat() ." + errormsg)

	# Making path an absolute and canonical path.
	# This also resolves symbolic links, so we don't use it if mustbe_symlink is True.
	# strongly requiring that realpath() also creates absolute paths like "abspath()" !
	if not mustbe_symlink:
		try:
			path = os.path.realpath(path, strict=True)
		except OSError as original_exc:
			raise UsageError("Path doesn't exist or contains a symlink loop or other comparable problems." + errormsg) from original_exc

	########################################
	# Beware using bare drive letters (e.g. "C:") on Windows as a path intended to point to the root directory of that windows-drive.
	# In some command line interpreters on windows the bare drive letter (e.g. "C:") of a windows-drive is resolved to the last CWD on that drive
	# (instead of the ROOT directory of that windows-drive).
	#
	# Solution: append directory separator symbol behind the bare drive letter
	#     => explicitly tell windows-CLI-interpreter to access the ROOT directory of that windows-drive!
	########################################
	if (mustbe_directory and    # noqa: W504 line break after binary operator
			os.name == 'nt' and    # noqa: W504 line break after binary operator
			len(path) == 2 and    # noqa: W504 line break after binary operator
			path[-1] == ':' and    # noqa: W504 line break after binary operator
			path[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
		path += os.sep
		_LOGGER.warning(f'We are operating on windows operating system and your path {path} is a bare drive letter. '
						'Some command line interpreters on windows resolve such a path to the last CWD used on that windows-drive '
						'(instead of the ROOT directory of that window-drive). '
						'Thus we append the directory separator symbol behind your path to explicitly tell any windows-CLI-interpreter '
						'to access the ROOT directory of that window-drive.')

	########################################
	# check is symlink, is dir, is file
	# Only considering symlinks, dirs and files (no fifos etc.) !
	#
	# Both os.path.isdir(path) and os.path.isfile(path) follow symbolic links, so both islink() and isdir()/isfile() can be true for the same path.
	# => first check for symbolic links and if mustbe_symlink is True, skip the checks of maybe_directory and maybe_file.
	########################################
	if mustbe_symlink and not os.path.islink(path):
		raise UsageError('Path must be symlink.' + errormsg)
	if not maybe_symlink and os.path.islink(path):
		raise UsageError('Path may NOT be symlink.' + errormsg)

	if mustbe_directory and not os.path.isdir(path):
		raise UsageError('Path must be directory.' + errormsg)
	if not mustbe_symlink:
		if not maybe_directory and os.path.isdir(path):
			raise UsageError('Path may NOT be directory.' + errormsg)

	if mustbe_file and not os.path.isfile(path):
		raise UsageError('Path must be file.' + errormsg)
	if not mustbe_symlink:
		if not maybe_file and os.path.isfile(path):
			raise UsageError('Path may NOT be file.' + errormsg)

	########################################
	# check access permissions of path
	########################################
	if mustbe_readable and not os.access(path, os.R_OK):
		raise UsageError('Path must be readable.' + errormsg)
	if not maybe_readable and os.access(path, os.R_OK):
		raise UsageError('Path may NOT be readable.' + errormsg)

	if mustbe_writable and not os.access(path, os.W_OK):
		raise UsageError('Path must be writable.' + errormsg)
	if not maybe_writable and os.access(path, os.W_OK):
		raise UsageError('Path may NOT be writable.' + errormsg)

	if mustbe_executable and not os.access(path, os.X_OK):
		raise UsageError('Path must be executable.' + errormsg)
	if not maybe_executable and os.access(path, os.X_OK):
		raise UsageError('Path may NOT be executable.' + errormsg)

	return path
