# Project sidlogism_python_toolbox

## What it does ##
This is a personal collection of small python tools frequently or occasionally needed in smaller python experiments and python scripts.


## Installation ##
Supported platforms: OpenBSD. Not tested on Windows & Linux (yet).

Just clone the git repo and import the modules by modifying your sys.path or your environment variable `PYTHONPATH` accordingly.
**We recommend using `PYTHONPATH` and `MYPYPATH`. See "Setting environment variables" and "Setting sys.path" below.**

### Hints for log configuration ###
When using a predefined log configuration file like in the code snippet below, be aware of the following effect of parameter `disable_existing_loggers` of function `logging.config.fileConfig()`.
If `disable_existing_loggers==True`, which is the default, all loggers that exist at the moment of calling `logging.config.fileConfig()` are disabled. This also includes loggers in **other, imported modules:** If you import modules which use internal **module-level loggers in the module scope** (i. e. outside any class or function definition like in the code snippet below) **before** calling `logging.config.fileConfig()`, all these internal module-level loggers of the imported modules **will be disabled as well since they were already constructed and existing beforehand when the corresponding import-statement was called.**

To avoid this you can either set `disable_existing_loggers=False` like in the code snippet below or you can move the line calling `logging.config.fileConfig()` **above** any import-statements of modules whose internal module-level logger you like to preserve.
For more details, see:
* https://docs.python.org/3/library/logging.config.html#logging.config.fileConfig
* https://stackoverflow.com/questions/35325042/python-logging-disable-logging-from-imported-modules/47685462#47685462

Logger config example from `test_logging_tools.py` using the idiom `_LOGGER = logging.getLogger(__name__)` to create an internal **module-level** logger:

	# configure logger for this script
	_LOGCONFIG_ENCODING: str = 'UTF-8'
	_LOGCONFIG_RELATIVE_PATH: str = 'src/sidlogism/python_toolbox/logging_default_config.ini'
	logging.config.fileConfig(_LOGCONFIG_RELATIVE_PATH, disable_existing_loggers=False, encoding=_LOGCONFIG_ENCODING)
	_LOGGER: Logger = logging.getLogger(__name__)
	_LOGGER.setLevel(logging.NOTSET)

### Setting environment variables ###
In order to avoid false-positive linter-errors caused by the import-discovery mechanisms of these linters not recognizing sys.path.append(), you have to set the environment variables `MYPYPATH` and `PYTHONPATH` (the latter for pylint).  **You also need to set `PYTHONPATH` if you want to avoid using sys.path.append() in your python scripts or unit tests altogether.**

Example on unix-like operating systems:

	# for python linter pylint:
	export PYTHONPATH="/home/myuser/Downloads/sidlogism_python_toolbox/src/"
	# for python linter mypy:
	export MYPYPATH="/home/myuser/Downloads/sidlogism_python_toolbox/src/"

**The used paths for the environment variables should be absolute paths since the relative path element `../` was not tested yet and the tilde symbol `~` as a shortcut for the user's home-dir is NOT supported in the environment variables, neither by mypy nor by pylint. Please keep in mind that if your IDE (e. g. VScode or PyCharm) uses internal linters, these linters must be made aware of the base paths for import-discovery as well.**

Instead of using the mentioned environment variables you could also resort to the below `mypy_path` config variable or to the `init-hook` config variable in pylint. But we are avoiding these config variables for two reasons. First, by placing hard-coded paths into the config files, we must always take care about not to accidentally committing these paths to git.
Second, for an unknown reason the `mypy_path` config variable is being ignored in `tox.ini`:

	[mypy]
	mypy_path = /home/myuser/Downloads/sidlogism_python_toolbox/src/


### Setting sys.path ###
Here is an sys.path-example:

	#!/usr/bin/env python3
	import sys
	sys.path.append('/home/myuser/Downloads/sidlogism_python_toolbox/src/')
	from sidlogism.python_toolbox import logging_tools
	from sidlogism.python_toolbox import subprocess_tools
	from sidlogism.python_toolbox.subprocess_tools import SubprocessRunner

You can also use a relative path in sys.path.append():

	import sys
	sys.path.append('../../Downloads/sidlogism_python_toolbox/src/')
	from sidlogism.python_toolbox import logging_tools
	...

or expansion-facilities for variables like os.path.expandvars() or os.path.expanduser():

	import sys
	import os
	sys.path.append(os.path.expanduser('~/Downloads/sidlogism_python_toolbox/src/'))
	from sidlogism.python_toolbox import logging_tools
	...

This also applies to the \_LOGCONFIG_RELATIVE_PATH that can be used in combination with logging_tools.py as seen in the corresponding unit test.

Instead of enabling import-discovery for the linters with the environment variables mentioned above, you could simply add check-ignores like the following in order to simply ignore all false-positive linter-errors related to import-discovery:

	#!/usr/bin/env python3
	# mypy: disable-error-code="import-not-found"
	import sys
	sys.path.append('/home/myuser/Downloads/sidlogism_python_toolbox/src/')
	from sidlogism.python_toolbox import logging_tools    # pylint: disable=import-error,wrong-import-position,no-name-in-module
	from sidlogism.python_toolbox import subprocess_tools    # pylint: disable=import-error,wrong-import-position,no-name-in-module
	from sidlogism.python_toolbox.subprocess_tools import SubprocessRunner    # pylint: disable=import-error,wrong-import-position,no-name-in-module


But even if you are using the above environment variables, for pylint and flake8, you still have to add the check-ignore comment `# pylint: disable=wrong-import-position # noqa: E402` after every import statement placed behind sys.path.append():

	#!/usr/bin/env python3
	import sys
	sys.path.append('/home/myuser/Downloads/sidlogism_python_toolbox/src/')
	from sidlogism.python_toolbox import logging_tools    # pylint: disable=wrong-import-position # noqa: E402
	from sidlogism.python_toolbox import subprocess_tools    # pylint: disable=wrong-import-position # noqa: E402
	from sidlogism.python_toolbox.subprocess_tools import SubprocessRunner    # pylint: disable=wrong-import-position # noqa: E402

* comment `# pylint: disable=wrong-import-position` is needed for pylint to ignore the error `C0413: Import "..." should be placed at the top of the module (wrong-import-position)`
* comment `# noqa: E402` is needed for flake8 to ignore the error `E402 module level import not at top of file`


---
_Side notes:_
* The project intentionally uses the so called "src layout" for a cleaner an more explicit import handling as pointed out in https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout
	* Possible workaround for making the "import package" directly executable: https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#running-a-command-line-interface-from-source-with-src-layout
* Currently the sidlogism_python_toolbox can only be installed in the described manual "ad hoc" manner. Distribution via PyPI as a fully fledged "distribution package" (with sdists and bdists) is not planned yet. 
	* However you can currently build the "distribution package" yourself by running the following command in the "distribution root" (see below): `python3 -m build`


## How to run the unit tests, doctests and linters automatically ##

* 1. You first need to install the linters listed in tox.ini. The automated pip-installation via tox-dependencies is omitted because on OpenBSD python "distribution packages" are installed via OS-packages (via pkg_add) instead of via pip.
* 2. After installation of the required linters, set the environment variables `PYTHONPATH` and `MYPYPATH` for import-discovery (see above and `tox.ini` for more details).
* 3. Finally, in "distribution root" (see definition below) run: `tox`
	* You can also run the `tox`-command in any subdirectory of "distribution root" (see definition below).
* 4. Customize `tox.ini` file for your purposes.
	* Place your own Python code for example in the `src/` subdirectory and your test code in the `tests/` subdirectory.
	* Alternatively, place your Python code in some other directory and adapt the commands and parameters for code discovery and import-discovery in `tox.ini` accordingly. See "src layout" below for more details.
    * **For importing the `\*\_tools.py` modules in your own Python modules consult our test modules in the `tests/` subdirectory and see "Setting environment variables" and "Setting sys.path" above.** 
	* Heed the `Hints for log configuration` above.


## How to run the unit tests, linters and the single doctests manually ##
* 1. First set the environment variables `PYTHONPATH` and `MYPYPATH` for import-discovery (see above and `tox.ini` for more details).
* 2. Second, run the desired linter command or test command. **See commands in tox.ini file for examples.**

Examples:
* In "distribution root" (see below) run: `python3 -Walways -m unittest discover -v -s tests`
* In "distribution root" (see below) run: `python3 -Walways -m unittest discover -v -s tests -p "test__misc_common_tools.py"`
* In "distribution root" (see below) run: `python3 -Walways -m doctest -v src/sidlogism/python_toolbox/*.py`
* In "import package" directory (see below) run: `python3 -Walways -m doctest -v subprocess_tools.py`


## License and usage limitations ##
The tools are free to use. No warranty or liability of any kind included. See license for details.

	Copyright 2025 Imperfect Silent Art
	SPDX-License-Identifier: Apache-2.0


## Terminology ##
For uniformity and simplicity, all documentation will stick to the following terminology:

* "import package" (or "simple package", "regular package", "Python package" or simply "package"):
	* e. g. folder "python_toolbox/" (in src/sidlogism/)
	* **Directory containing an "\_\_init\_\_.py" file (and further Python modules).**
	* in accordance with the PyPA-terminology:
		* https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
			* "Regular import packages have an \_\_init\_\_.py."
        * https://packaging.python.org/en/latest/glossary/#term-Import-Package
		* https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/
		* https://packaging.python.org/en/latest/tutorials/packaging-projects/
			* name origin: "[...] the existence of an \_\_init\_\_.py file allows users to import the directory as a regular package, [...]"
        * legacy documentation: https://docs.python.org/3.11/distutils/introduction.html#concepts-terminology
			* "package: a module that contains other modules; typically contained in a directory in the filesystem and distinguished from other directories by the presence of a file \_\_init\_\_.py."

* "namespace package"
	* **e. g. all "sidlogism" directories without "\_\_init\_\_.py" file**
	* see "Native namespace packages" on: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/

* "distribution root" directory (or "project root" directory)
	* **Directory containing the pyproject.toml and tox.ini files. This is also the base directory of the git repository for project "sidlogism_python_toolbox".**
	* in accordance with the PyPA-terminology: https://docs.python.org/3.11/distutils/introduction.html#concepts-terminology

* "src layout"/"src-layout", see:
	* https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout
	* https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/#src-layout-vs-flat-layout

* "distribution package" (or "(module) distribution" or simply "project"):
	* e. g. the "NumPy" or "SciPy" libraries in the PyPI
	* **A Python library (collection of Python modules) that you can download and install as a single "distribution" unit (e. g. from PyPI).**
	* in accordance with the PyPA-terminology:
		* https://packaging.python.org/en/latest/glossary/#term-Distribution-Package
			* "A versioned archive file that contains Python packages, modules, and other resource files that are used to distribute a Release. The archive file is what an end-user will download from the internet and install."
		* https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/
			* "A distribution package is a piece of software that you can install."
			* "Alternatively, the term “distribution package” can be used to refer to a specific file that contains a certain version of a project."
		* legacy documentation: https://docs.python.org/3.11/distutils/introduction.html#concepts-terminology
        	* "module distribution: a collection of Python modules distributed together as a single downloadable resource and meant to be installed en masse."
