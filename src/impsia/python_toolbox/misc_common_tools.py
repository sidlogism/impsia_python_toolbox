"""Miscellaneous tools which cover different problem domains and topics or wich are commonly used by the other tools in the toolbox."""
import os
import sys

if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)


ERRNO_SUCCESS = 0
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_SUCCESS = os.EX_OK
except AttributeError:
	pass

ERRNO_UNKNOWN = 1
try:
	# Not all os.EX_... errnos are available on Windows => accessing them might throw an exception on Windows
	ERRNO_UNKNOWN = os.EX_SOFTWARE
except AttributeError:
	pass
__all__ = ['ERRNO_SUCCESS', 'ERRNO_UNKNOWN', 'ImpsiaError', 'UsageError', 'strip_fileextension']


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
