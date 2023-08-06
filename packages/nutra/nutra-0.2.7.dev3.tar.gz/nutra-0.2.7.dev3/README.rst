********************
 nutratracker (cli)
********************

Command line tools for interacting with government food database,
and analyzing your health trends. The ``SR28`` database includes data
for ~8500 foods and ~180 nutrients. Customizable with extensions
and mapping rules built on top.

**Requires:**

- Python 3.4.0 or later (``lzma``, ``ssl`` & ``sqlite3`` modules)
  [Win XP / Ubuntu 14.04].
- Packages: see ``setup.py``, and ``requirements.txt`` files.
- Internet connection, to download food database & package dependencies.

See ``nt`` database:   https://github.com/nutratech/nt-sqlite

See ``usda`` database: https://github.com/nutratech/usda-sqlite


Details
#######################################################

.. list-table::
  :widths: 15 25 20
  :header-rows: 1

  * - Category
    -
    -
  * - Install / Linux
    - .. image:: https://github.com/nutratech/cli/actions/workflows/install-linux.yml/badge.svg
        :target: https://github.com/nutratech/cli/actions/workflows/install-linux.yml
        :alt: Test status unknown (Linux)
    -
  * - Install / Windows
    - .. image:: https://github.com/nutratech/cli/actions/workflows/install-win32.yml/badge.svg
        :target: https://github.com/nutratech/cli/actions/workflows/install-win32.yml
        :alt: Test status unknown (Windows)
    -
  * - Other checks
    - .. image:: https://coveralls.io/repos/github/nutratech/cli/badge.svg?branch=master
        :target: https://coveralls.io/github/nutratech/cli?branch=master
        :alt: Coverage unknown
    - .. image:: https://github.com/nutratech/cli/actions/workflows/lint.yml/badge.svg
        :target: https://github.com/nutratech/cli/actions/workflows/lint.yml
        :alt: Lint status unknown
  * - PyPI Release
    - .. image:: https://badgen.net/pypi/v/nutra
        :target: https://pypi.org/project/nutra/
        :alt: Latest version unknown
    - .. image:: https://pepy.tech/badge/nutra/month
        :target: https://pepy.tech/project/nutra
        :alt: Monthly downloads unknown
  * - Supported Runtime
    - .. image:: https://img.shields.io/pypi/pyversions/nutra.svg
        :alt: Python3 (3.4 - 3.10)
    -
  * - Code Style
    - .. image:: https://badgen.net/badge/code%20style/black/000
        :target: https://github.com/ambv/black
        :alt: Code style: black
    -
  * - License
    - .. image:: https://badgen.net/pypi/license/nutra
        :target: https://www.gnu.org/licenses/gpl-3.0.en.html
        :alt: License GPL-3
    -


Linux / macOS requirements (for development)
#######################################################

You will need to install ``make`` and ``gcc`` to build the ``Levenshtein``
extension.

::

  sudo apt install \
    make gcc \
    python3-dev python3-venv \
    direnv


You can add the ``direnv`` hook, ``direnv hook bash >>~/.bashrc``.
Only run this once.


Plugin Development
#######################################################

You can develop plugins (or data modifications sets) that
are imported and built on the base (or core) installation.

These currently can take the form of custom recipes, foods, and RDA injection.


Supporting Old Versions of Python
#######################################################

The old requirements can still be tested on modern interpreters.
Simply install them with this (inside your ``venv`` environment).

::

  pip install -r requirements-old.txt

This won't guarantee compatibility for every version, but it will help.
We provide a wide range. The oldest version of ``tabulate`` is from 2013.

There is automated testing on GitHub, but to use an old interpreter
(Python 3.4 does not have the ``typing`` module! Only ``collections.abc``),
you may need to use a virtual machine or install old SSL libraries or enter a
similar messy state.
My preference is for VirtualBox images, where I manually test *Windows XP*
& *Ubuntu 14.04*.


Notes
#######################################################

On Windows you should check the box during the Python installer
to include ``Scripts`` directory in your ``%PATH%``.  This can be done
manually after installation too.

Windows users may also have differing results if they install for all users
(as an administrator) vs. installing just for themselves. It may change the
location of installed scripts, and affect the ``$PATH`` variable being
correctly populated for prior installs.

Linux may need to install ``python-dev`` package to build
``python-Levenshtein``.
I am currently debating making this an optional dependency to avoid
confusing install failures for people without ``gcc`` or ``python3-dev``.

Windows users may not be able to install ``python-Levenshtein``.

Main program works 100%, but ``test`` and ``lint`` may break on older operating
systems (*Ubuntu 14.04*, *Windows XP*).


Install PyPi release (from pip)
#######################################################

.. code-block:: bash

  pip install -U nutra

(**Specify:** flag ``-U`` to upgrade, or ``--pre`` for development releases)


Using the source code directly
#######################################################

Clone down, initialize ``nt-sqlite`` submodule, and install requirements:

.. code-block:: bash

  git clone https://github.com/nutratech/cli.git
  cd cli
  make init
  # source .venv/bin/activate  # uncomment if NOT using direnv
  make deps

  ./nutra -h


Initialize the DBs (``nt`` and ``usda``).

.. code-block:: bash

  # source .venv/bin/activate  # uncomment if NOT using direnv
  ./nutra init

  # Or install and run as package script
  make install
  n init


If installed (or inside ``cli``) folder, the program can also run
with ``python -m ntclient``.

You may need to set the ``PY_SYS_INTERPRETER`` value for the ``Makefile``
if trying to install other than with ``/usr/bin/python3``.

Building the PyPi release (sdist)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  # source .venv/bin/activate  # uncomment if NOT using direnv
  make build  # python3 setup.py --quiet sdist
  twine upload dist/nutra-X.X.X.tar.gz


Linting & Tests
#######################################################

Install the dependencies (``make deps``). Now you can lint & test.

.. code-block:: bash

  # source .venv/bin/activate  # uncomment if NOT using direnv
  make format lint test


ArgComplete (tab completion / autocomplete)
#######################################################

The ``argcomplete`` package will be installed alongside.


Linux, macOS, and Linux Subsystem for Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simply run the following out of a ``bash`` shell. Check their page for more
specifics on using other shells, e.g. ``zsh``, ``fish``, or ``tsh``.

.. code-block:: bash

  activate-global-python-argcomplete --user

Then you can press tab to fill in or complete sub-commands
and to list argument flags.


Windows (Git Bash)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This can work with git bash too. I followed the instructions on their README.

I've run the command to seed the autocomplete script.

.. code-block:: bash

  mkdir -p $HOME/.bash_completion.d
  activate-global-python-argcomplete --user


And my ``~/.bashrc`` file looks like this.

.. code-block:: bash

  export ARGCOMPLETE_USE_TEMPFILES=1

  # python bash completion
  if [ -f ~/.bash_completion.d/python-argcomplete ]; then
      source ~/.bash_completion.d/python-argcomplete
  fi


**NOTE:** Standard autocomplete is fully functional, we are adding customized
completions


Currently Supported Data
#######################################################

**USDA Stock database**

- Standard reference database (SR28)  **[7794 foods]**

**USDA Extensions (Relational)**

- Flavonoid, Isoflavonoids, and Proanthocyanidins  **[1352 foods]**


Usage
#######################################################

Requires internet connection to download initial datasets.
Run ``nutra init`` for this step.

Run ``n`` or ``nutra`` to output usage (``-h`` flag is optional and defaulted).
