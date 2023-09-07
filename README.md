<!--
SPDX-FileCopyrightText: 2023 Joni Hyttinen <joni.hyttinen@uef.fi>

SPDX-License-Identifier: CC-BY-NC-SA-4.0
-->

# Signal analyzer template
This repository contains a project template that can be used as a base for your
own solution. The application is written in [Python](https://www.python.org) and
[Qt for Python](https://doc.qt.io/qtforpython-6/), and utilizes [numpy](https://numpy.org/) 
for computational tasks.

## Python and virtual environments
Python ecosystem has multiple ways to install and use packages. Especially
for Windows and macOS users, a fairly simple to install Python distribution
is [Anaconda](https://anaconda.com). Linux-users may find Anaconda or its
package manager **conda** in their distribution's package repository.

Another option is to use the system Python.
- On Windows, one can find **Python 3.11** in *Microsoft Store* and install it
  from there; 
- On Linux, the distribution should provide **Python 3.11** in their package
  repository;
- On macOS, a third-party package repository, [Homebrew](https://brew.sh/), can
  be used to install the current **Python 3.11**.

### Setting up a Conda virtual environment

- Create a minimal new virtual environment:

  ``conda create -n idp2023 python=3.11``

- Install **PySide6**

  ``conda install -n idp2023 pyside6 -c conda-forge``

- Install the other dependencies

  ``conda install -n idp2023 numpy``

- Updating the environment can be done with

  ``conda update -n idp2023 --all``

  > Note, however, that the update will replace some packages installed from
  > **conda-forge**. This should be fine as long as `conda` is not attempting
  > to remove the **pyside6**-package.

- Download or `git clone` the project on your system.
- Open it the development environment of your choice.
- Choose the newly created **idp2023** virtual environment as your project's
  Python environment.

### Setting up a Poetry virtual environment
This approach uses the system Python. We recommend that you first install a
tool to manage Python applications: [pipx](https://pypa.github.io/pipx/). The
**pipx**-tool is used to install Python applications in their own dedicated
virtual environments.

- Install **pipx**
  
  ``python3.11 -m pip install --user pipx``

The project is described in **pyproject.toml**, which includes descriptions of
the needed dependencies and scripts to run the project for [Poetry](https://python-poetry.org/)
packaging and dependency management tool.

- Install **poetry**

  ``pipx install poetry``

- \[Optional\] By default, on Windows, **poetry** creates project virtual 
  environments in a difficult to find path. Configure the virtual environment
  location to use an easier path.

  | Shell          | Command                                                                 |
  |----------------|-------------------------------------------------------------------------|
  | Command prompt | ``poetry config virtualenvs.path %USERPROFILE%\.virtualenvs-poetry``    |
  | PowerShell     | ``poetry config virtualenvs.path $env:USERPROFILE\.virtualenvs-poetry`` |

  Now you can remove all virtual environments created by **poetry** by simply
  removing the **.virtualenvs-poetry** directory in your user profile (C:\Users\Username).

- Download or `git clone` the project on your system
- In the project folder, create the project virtual environment
  
  `poetry install`

- Open the project in your chosen development environment and use Poetry integration,
  if such is available, to manage the virtual environment.

## File tree
- idp2023_example

  The source code for the project.

  - \_\_init\_\_.py
  
    Package initialization code. Empty file.

  - signal\_analyzer.py

    A signal analyzer class whose instances are run in worker threads.
    Communicates with the user interface code through signals.
  
  - signal\_app\_main\_window.py
  
    The main class of the application. Composes the main window and contains
    program main methods. The main widget is in a separate class.

  - signal\_app\_widget.py
  
    The main widget of the application. The instantiated main class of the
    application creates an instance of this class as its center widget.

  - signal\_window\_chart\_widget.py
    
    A simple chart widget for showing a signal.

  - worker.py
  
    A helper class to construct worker threads.

  - worker\_signals.py
  
    A helper class' helper class. Defines the signals that a worker thread
    may emit after a successful completion, an exception, or for progress
    indication.
  
- pyproject.toml

  Project file for ``poetry``-build system.

- poetry.lock

  The exact Python packages that are or should be installed in a virtual
  environment managed by ``poetry``.

- README.md
  
  This file.

## Extending the template

Tasks to solve the industrial problem by extending the template could include:
- Investigate the suitability of [SciPy](https://scipy.org/) for signal processing tasks?
  
  | Environment manager | Command                          |
  |---------------------|----------------------------------|
  | Anaconda            | `conda -n idp2023 install scipy` |
  | Poetry              | `poetry add scipy`               |

- Add code to open a saved signal file?
- Add code read a saved signal file?
  - Perhaps it is not necessary to read the whole file into memory at once..?
    - windowing functions?
    - memory mapping?
- Edit **signal\_analyzer.py** to do something useful
- Extend the user interface to show positive detections?
- Extend the application to count positive/false detections using a ground
  truth file?
- Switch **QtCharts** to something more capable?

