"""Perfrom package-wide initializations."""
import os
import sys

if __name__ == "__main__":
	# exit execution and indicate error
	print("ERROR: this module is not intended for direct execution as standalone script.")
	sys.exit(os.EX_USAGE)
