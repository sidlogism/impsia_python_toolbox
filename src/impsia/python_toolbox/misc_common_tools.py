"""Miscellaneous tools which cover different problem domains and topics or wich are commonly used by the other tools in the toolbox."""
import os
import sys
import re
import logging
from logging import Logger

if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)


_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.NOTSET)


ERRNO_SUCCESS: int = 0
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_SUCCESS = os.EX_OK
except AttributeError:
	pass

ERRNO_UNKNOWN: int = 1
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_UNKNOWN = os.EX_SOFTWARE
except AttributeError:
	pass
__all__: list[str] = ['ERRNO_SUCCESS', 'ERRNO_UNKNOWN', 'ImpsiaError', 'UsageError',
	'strip_fileextension', 'sanitize_input_string', 'sanitize_userinput_path']


class ImpsiaError(Exception):
	"""Generic excpetion base class for customized exception types."""

	errno = ERRNO_UNKNOWN

	def __init__(self, msg):
		"""Initizalize ImpsiaError object."""
		self.msg = msg

	def __str__(self):
		"""Paraphrase ImpsiaError object as string."""
		return self.msg


class UsageError(ImpsiaError):
	"""Customized exception type for usage errors."""

	errno = 2

	def __init__(self, msg):
		"""Initizalize UsageError object."""
		super().__init__(msg)
		try:
			# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
			type(self).errno = os.EX_USAGE
		except AttributeError:
			pass


def strip_fileextension(file_basename: str) -> str:
	"""Strip file extension from filename."""
	if file_basename.startswith('./') or file_basename.startswith(os.curdir + os.sep):
		# strip leading './'
		file_basename = file_basename[2:]
	if os.sep in file_basename:
		raise UsageError(f'The given file base name "{file_basename}" is invalid because it seems to contain some path fragments. '
			'It contains the directory separator symbol "{os.sep}" for separating directories within filesystem paths.')
	stripped_basename: str = os.path.splitext(os.path.basename(file_basename))[0]
	return stripped_basename


def sanitize_input_string(user_string: str, encoding: str, whitelist: str, blacklist: str) -> None:
	"""Sanitize given user input string by throwing exception if undesired characters or encodings are detected within string."""
	# Throws an UnicodeEncodeError if unsupported chars are within user input string !
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
	Sanitize given path from user input by checking whether path exists and attributes are as expected or whether path contains undesired characters.

	Mind the "mustbe"-flags and "maybe"-flags! Per default they are all set to False, which simply disqualifies all paths!
	Thus you must set the suitable "mustbe"-flags and "maybe"-flags for your use case to True!
	If a "mustbe"-flag is True, the corresponding "maybe"-flag will be automatically set to True.

	This function is only considering symlinks, directories and files. Fifos and special device files etc. are not supported!

	Raises:
		UsageError: if path doesn't exist, doesn't have expected attributes (type and access permissions) or if path contains undesired characters.
	"""
	# maybe_suid_executable=False
	########################################
	# possible test paths:
	#
	# C:\Program Files\Common Files
	# \;\&\'"#$%C:\Program Files\Common Files/~/foo-bar_baz/1234567890\u00c4\u00d6\u00dc\u00df\u00e4\u00f6\u00fc.txt"
	# + umlauts
	# ~/Arbeitsflaeche/
	# /usr/bin/apt-get
	########################################

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
	whitelist += r'\. \-_'  # valid directoryname of filename components (space too, though deprecated , but NOT other whitespace !!)
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

	# strongly requiring that realpath() also creates absolute paths like "abspath()" !
	path = os.path.realpath(path)

	########################################
	# Beware using bare drive letters (e.g. "C:") on Windows as a path intented to point to the root directory of that windows-drive.
	# In some command line interpreters on windows the bare drive letter (e.g. "C:") of a windows-drive is resolved to the last CWD on that drive
	# (instead of the ROOT directory of that window-drive).
	#
	# Solution: append directory separator symbol behind the bare drive letter
	#     => explicitly tell windows-CLI-interpreter to access the ROOT directory of that window-drive!
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

	########################################
	# check is symlink, is dir, is file
	# Only considering symlinks, dirs and files (no fifos etc.) !
	#
	# os.path.isdir(path)
	# This follows symbolic links, so both islink() and isdir() can be true for the same path.
	# => first check for symbolic links !!
	########################################
	if mustbe_symlink and not os.path.islink(path):
		raise UsageError('Path must be symlink.' + errormsg)
	if not maybe_symlink and os.path.islink(path):
		raise UsageError('Path may NOT be symlink.' + errormsg)

	if mustbe_directory and not os.path.isdir(path):
		raise UsageError('Path must be directory.' + errormsg)
	if not maybe_directory and os.path.isdir(path):
		raise UsageError('Path may NOT be directory.' + errormsg)

	if mustbe_file and not os.path.isfile(path):
		raise UsageError('Path must be file.' + errormsg)
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
