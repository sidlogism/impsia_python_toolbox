# Project impsia_python_toolbox

## What it does ##
This is a personal to use collection of small python tools frequently or occasionally needed in smaller python experiments and python scripts.
Supported platforms: OpenBSD. Not tested on Windows & Linux (yet).

## Installation ##
Just clone the git repo. This downloads the 'impsia_python_toolbox' directory containing the '__init__.py' file, which we call 'package directory'. We call the parent directory of the 'package directory' the 'distribution root' directory in accordance with the PyPA-terminology (https://docs.python.org/3.11/distutils/introduction.html#concepts-terminology). It is the directory containing the setup.py file and also the base directory of the git repository for project 'impsia_python_toolbox'.
For package installation either simply copy the 'package directory' somewhere in your sys.path or change your sys.path or environment variable PYTHONPATH accordingly.

Side note: Currently these tools can only be installed in the described manual 'ad hoc' manner. Maybe in the future this package might be bundled into a fully fledged python package with sdists and bdists for distribution on PyPY. But that's not planned yet. 

## How to run the sample application ##
See 'supported platforms' above!

## How to run the unittests and the single doctests manually ##
In 'distribution root' (see above) run: python3 -m unittest discover -v -s tests
In 'package directory' run: python3 -m doctest -v impsia_subprocess_handling.py

## License and usage limitations ##
The tools are free to use. No warranty or liability of any kind included. See license for details.
