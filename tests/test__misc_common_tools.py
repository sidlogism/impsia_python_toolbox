#!/usr/bin/env python3
"""Unit test cases for testing the miscellaneous common tools of impsia_python_toolbox."""

import os
import tempfile
import unittest
import logging
from logging import Logger
from impsia.python_toolbox.misc_common_tools import sanitize_userinput_path, sanitize_input_string, strip_fileextension, UsageError

_LOGGER: Logger = logging.getLogger(__name__)
_LOGGER.setLevel(logging.NOTSET)

__all__: list[str] = ['TestMiscCommonTools']


class TestMiscCommonTools(unittest.TestCase):
	"""Test miscellaneous common tools."""

	def setUp(self) -> None:
		"""Set up temporary test files and directories."""
		# Create a temporary directory
		self.temp_dir = tempfile.mkdtemp()

		# Create a temporary file
		self.temp_file_fd, self.temp_file_path = tempfile.mkstemp(dir=self.temp_dir)
		os.close(self.temp_file_fd)

		# Create a temporary symlink (if supported by OS)
		self.temp_symlink_path = os.path.join(self.temp_dir, "symlink_test")
		try:
			os.symlink(self.temp_file_path, self.temp_symlink_path)
			self.symlinks_supported = True
		except (OSError, AttributeError):
			self.symlinks_supported = False

	def tearDown(self) -> None:
		"""Clean up temporary files and directories."""
		# Remove symlink if it exists and is supported
		if self.symlinks_supported and os.path.exists(self.temp_symlink_path):
			os.unlink(self.temp_symlink_path)

		# Remove temporary file
		if os.path.exists(self.temp_file_path):
			os.unlink(self.temp_file_path)

		# Remove temporary directory
		if os.path.exists(self.temp_dir):
			os.rmdir(self.temp_dir)

	def test_sanitize_userinput_path__valid_file(self) -> None:
		"""Test sanitize_userinput_path with valid file path."""
		result = sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_file=True,
										maybe_readable=True,
										maybe_writable=True,
										maybe_executable=True)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected canonical path.')

	def test_sanitize_userinput_path__valid_directory(self) -> None:
		"""Test sanitize_userinput_path with valid directory path."""
		result = sanitize_userinput_path(self.temp_dir, 'UTF-8', mustbe_directory=True,
										maybe_readable=True,
										maybe_writable=True,
										maybe_executable=True)
		self.assertEqual(result, os.path.realpath(self.temp_dir),
						'The sanitized path does not match the expected canonical path.')

	def test_sanitize_userinput_path__valid_symlink(self) -> None:
		"""Test sanitize_userinput_path with valid symlink path."""
		if not self.symlinks_supported:
			self.skipTest("Symlinks not supported on this platform")

		result = sanitize_userinput_path(self.temp_symlink_path, 'UTF-8', mustbe_symlink=True,
										maybe_readable=True,
										maybe_writable=True,
										maybe_executable=True)
		self.assertEqual(result, self.temp_symlink_path,
						'The sanitized path does not match the expected symlink path.')

	def test_sanitize_userinput_path__conflicting_requirements(self) -> None:
		"""Test sanitize_userinput_path with conflicting requirements."""
		with self.assertRaises(UsageError):
			sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_file=True, mustbe_directory=True,
									maybe_readable=True,
									maybe_writable=True,
									maybe_executable=True)

		with self.assertRaises(UsageError):
			sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_file=True, mustbe_symlink=True,
									maybe_readable=True,
									maybe_writable=True,
									maybe_executable=True)

		with self.assertRaises(UsageError):
			sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_directory=True, mustbe_symlink=True,
									maybe_readable=True,
									maybe_writable=True,
									maybe_executable=True)

	def test_sanitize_userinput_path__nonexistent_path(self) -> None:
		"""Test sanitize_userinput_path with nonexistent path."""
		nonexistent_path = os.path.join(self.temp_dir, "nonexistent_file.txt")
		with self.assertRaises(UsageError):
			sanitize_userinput_path(nonexistent_path, 'UTF-8', mustbe_file=True,
									maybe_readable=True,
									maybe_writable=True,
									maybe_executable=True)

	def test_sanitize_userinput_path__readable(self) -> None:
		"""Test sanitize_userinput_path with readable requirement."""
		# Make file readable (should be by default)
		os.chmod(self.temp_file_path, 0o444)

		result = sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_readable=True,
										maybe_file=True,
										maybe_writable=False,
										maybe_executable=False)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected canonical path.')

	def test_sanitize_userinput_path__writable(self) -> None:
		"""Test sanitize_userinput_path with writable requirement."""
		# Make file writable
		os.chmod(self.temp_file_path, 0o222)

		result = sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_writable=True,
										maybe_file=True,
										maybe_readable=False,
										maybe_executable=False)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected canonical path.')

	def test_sanitize_userinput_path__executable(self) -> None:
		"""Test sanitize_userinput_path with executable requirement."""
		# Make file executable
		os.chmod(self.temp_file_path, 0o111)

		result = sanitize_userinput_path(self.temp_file_path, 'UTF-8', mustbe_executable=True,
										maybe_file=True,
										maybe_readable=False,
										maybe_writable=False)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected canonical path.')

	def test_sanitize_userinput_path__invalid_requirement(self) -> None:
		"""Test sanitize_userinput_path with impossible file requirement."""
		with self.assertRaises(UsageError):
			sanitize_userinput_path(self.temp_dir, 'UTF-8', mustbe_file=True,
									maybe_readable=True,
									maybe_writable=True,
									maybe_executable=True)

	def test_sanitize_userinput_path__windows_drive_letter(self) -> None:
		"""Test sanitize_userinput_path with Windows drive letter."""
		if os.name != 'nt':
			self.skipTest("Test only relevant on Windows")

		# This test only runs on Windows where drive letters are used
		# For example, if we have a C: drive
		drive_letter = 'C:'
		result = sanitize_userinput_path(drive_letter, 'UTF-8', mustbe_directory=True,
										maybe_readable=True,
										maybe_writable=True,
										maybe_executable=True)
		self.assertEqual(result, drive_letter + os.sep,
						'The sanitized path should append directory separator to drive letter.')

	def test_sanitize_input_string__valid_string(self) -> None:
		"""Test sanitize_input_string with valid string."""
		test_string = "valid_string-123.txt"
		whitelist = r'\w\.\-_'
		blacklist = r';&#'

		# If no exception is raised, the test passes
		sanitize_input_string(test_string, 'utf-8', whitelist, blacklist)

	def test_sanitize_input_string__invalid_string(self) -> None:
		"""Test sanitize_input_string with invalid string."""
		test_string = "invalid_string;with#blacklisted&chars"
		whitelist = r'\w\.\-_'
		blacklist = r';&#'

		with self.assertRaises(UsageError):
			sanitize_input_string(test_string, 'utf-8', whitelist, blacklist)

	def test_strip_fileextension__valid_filename(self) -> None:
		"""Test strip_fileextension with valid file basename."""
		file_basename: str = "./valid_string-123.txt"

		result: str = strip_fileextension(file_basename)
		self.assertEqual(result, "valid_string-123", 'The stripped file basename does not match the expected value.')

	def test_strip_fileextension__invalid_filename(self) -> None:
		"""Test strip_fileextension with invalid file basename."""
		file_basename: str = "valid_string/123.txt"

		with self.assertRaises(UsageError):
			strip_fileextension(file_basename)


if __name__ == '__main__':
	unittest.main()
