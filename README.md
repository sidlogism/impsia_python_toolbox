# Project impsia_python_toolbox

## What it does ##
This is a personal to use collection of small python tools frequently or occasionally needed in smaller python experiments and python scripts.
Supported platforms: OpenBSD. Not tested on Windows & Linux (yet).

## Installation ##
Just clone the git repo. This downloads the 'impsia_python_toolbox' directory containing the '__init__.py' file, which we call 'package directory'. We call the parent directory of the 'package directory' the 'base directory' or 'project root'.
Either copy this 'package directory' somewhere in your sys.path or change your sys.path accordingly.

Side note: Even though the 'package directory' could be finalized with a setup.py file and wrapped into a fully fledged python package for distribution on PyPY but that's not planned yet. Currently these tools are only used in the described 'ad hoc' manner.

## How to run the sample application ##
See 'supported platforms' above!

## How to run the unittests ##
Navigate to the 'base directory' (see above) and run: python3 -m unittest discover -s tests -v

## License and usage limitations ##
The tools are free to use. No warranty or liability of any kind included. See license for details.
