# Project impsia_python_toolbox

## What it does ##
This is a personal to use collection of small python tools frequently or occasionally needed in smaller python experiments and python scripts.


## Installation ##
Supported platforms: OpenBSD. Not tested on Windows & Linux (yet).

Just clone the git repo and import the modules by modifying your sys.path or environment variable PYTHONPATH accordingly.
Here is an example:
#!/usr/bin/env python3

import sys
sys.path.append('/home/myuser/Downloads/impsia_python_toolbox/src/')
import impsia.python_toolbox
import impsia.python_toolbox.subprocess_tools
from impsia.python_toolbox.subprocess_tools import SubprocessRunner

Side notes:
* The project intentionally uses the so called "src layout" for a cleaner an more epxlicit import handling as pointed out in https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout
** Possible workaround for making the "import package" directly executable: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#running-a-command-line-interface-from-source-with-src-layout
* Currently these tools can only be installed in the described manual "ad hoc" manner. Distribution via PyPY as a fully fledged "distribution package" (with sdists and bdists) is not planned yet. 
** However you can currently build the "distribution package" yourself by running the following command in the "distribution roo" (see below): python3 -m build

## How to run the unittest, doctests an linters automatically ##

TODO


## How to run the unittests and the single doctests manually ##
In "distribution root" (see below) run: python3 -m unittest discover -v -s tests
In "import package" directory run: python3 -m doctest -v subprocess_tools.py


## License and usage limitations ##
The tools are free to use. No warranty or liability of any kind included. See license for details.


## Terminology ##
For uniformity and simplicitiy, all documentation will stick to the following terminology:

* "import package" (or regular, simple package):
** e. g. folder impsia/python_toolbox/
** Directory containing a "__init__.py" file (and further python modules).
** in accordance with the PyPA-terminology:
- https://packaging.python.org/en/latest/glossary/#term-Import-Package
- https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/
- https://packaging.python.org/en/latest/tutorials/packaging-projects/

* "namespace package"
** e. g. all "impsia" directories without "__init__.py" file
** see: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/

* "distribution root" directory (or "project root" directory)
** Directory containing the setup.cfg file and also the base directory of the git repository for project "impsia_python_toolbox".
** in accordance with the PyPA-terminology: https://docs.python.org/3.11/distutils/introduction.html#concepts-terminology

* "src layout"/"src-layout", see:
** https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout
** https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout
