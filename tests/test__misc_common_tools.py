#!/usr/bin/env python3
"""Unit test cases for testing the miscellaneous common tools of impsia_python_toolbox."""

import os
import sys
import tempfile
import unittest
import logging
from logging import Logger
from typing import Any
from impsia.python_toolbox.misc_common_tools import sanitize_path, sanitize_input_string, UsageError

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

	def test_sanitize_path__valid_file(self) -> None:
		"""Test sanitize_path with valid file path."""
		result = sanitize_path(self.temp_file_path, mustbe_file=True)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected real path.')

	def test_sanitize_path__valid_directory(self) -> None:
		"""Test sanitize_path with valid directory path."""
		result = sanitize_path(self.temp_dir, mustbe_directory=True)
		self.assertEqual(result, os.path.realpath(self.temp_dir),
						'The sanitized path does not match the expected real path.')

	def test_sanitize_path__valid_symlink(self) -> None:
		"""Test sanitize_path with valid symlink path."""
		if not self.symlinks_supported:
			self.skipTest("Symlinks not supported on this platform")

		result = sanitize_path(self.temp_symlink_path, mustbe_symlink=True)
		self.assertEqual(result, os.path.realpath(self.temp_symlink_path),
						'The sanitized path does not match the expected real path.')

	def test_sanitize_path__conflicting_requirements(self) -> None:
		"""Test sanitize_path with conflicting requirements."""
		with self.assertRaises(UsageError):
			sanitize_path(self.temp_file_path, mustbe_file=True, mustbe_directory=True)

		with self.assertRaises(UsageError):
			sanitize_path(self.temp_file_path, mustbe_file=True, mustbe_symlink=True)

		with self.assertRaises(UsageError):
			sanitize_path(self.temp_file_path, mustbe_directory=True, mustbe_symlink=True)

	def test_sanitize_path__nonexistent_path(self) -> None:
		"""Test sanitize_path with nonexistent path."""
		nonexistent_path = os.path.join(self.temp_dir, "nonexistent_file.txt")
		with self.assertRaises(UsageError):
			sanitize_path(nonexistent_path)

	def test_sanitize_path__readable(self) -> None:
		"""Test sanitize_path with readable requirement."""
		# Make file readable (should be by default)
		os.chmod(self.temp_file_path, 0o444)

		result = sanitize_path(self.temp_file_path, mustbe_readable=True)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected real path.')

	def test_sanitize_path__writable(self) -> None:
		"""Test sanitize_path with writable requirement."""
		# Make file writable
		os.chmod(self.temp_file_path, 0o666)

		result = sanitize_path(self.temp_file_path, mustbe_writable=True)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected real path.')

	def test_sanitize_path__executable(self) -> None:
		"""Test sanitize_path with executable requirement."""
		# Make file executable
		os.chmod(self.temp_file_path, 0o777)

		result = sanitize_path(self.temp_file_path, mustbe_executable=True)
		self.assertEqual(result, os.path.realpath(self.temp_file_path),
						'The sanitized path does not match the expected real path.')

	def test_sanitize_path__invalid_requirement(self) -> None:
		"""Test sanitize_path with impossible file requirement."""
		with self.assertRaises(UsageError):
			sanitize_path(self.temp_dir, mustbe_file=True)

	def test_sanitize_path__windows_drive_letter(self) -> None:
		"""Test sanitize_path with Windows drive letter."""
		if os.name != 'nt':
			self.skipTest("Test only relevant on Windows")

		# This test only runs on Windows where drive letters are used
		# For example, if we have a C: drive
		drive_letter = 'C:'
		result = sanitize_path(drive_letter, mustbe_directory=True)
		self.assertEqual(result, drive_letter + os.sep,
						'The sanitized path should append directory separator to drive letter.')

	def test_sanitize_input_string__valid_string(self) -> None:
		"""Test sanitize_input_string with valid string."""
		test_string = "valid_string-123.txt"
		whitelist = r'\w\.\-_'
		blacklist = r';&#'

		# If no exception is raised, the test passes
		sanitize_input_string(test_string, 'utf-8', whitelist, blacklist)
		self.assertTrue(True)  # Just to assert something

	def test_sanitize_input_string__invalid_string(self) -> None:
		"""Test sanitize_input_string with invalid string."""
		test_string = "invalid_string;with#blacklisted&chars"
		whitelist = r'\w\.\-_'
		blacklist = r';&#'

		with self.assertRaises(UsageError):
			sanitize_input_string(test_string, 'utf-8', whitelist, blacklist)


if __name__ == '__main__':
	unittest.main()
