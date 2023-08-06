# jetto-pythontools

Python tools for plotting and manipulating JETTO runs.

## A word of caution

These tools are a community collaboration under development, and probably always will be. 
If you want to report a problem or ask for a feature, please 
[open an issue at JET](https://git.ccfe.ac.uk/jintrac/jetto-pythontools/issues) or [gitlab.com](https://gitlab.com/jintrac/jetto-pythontools),
so the responsible person can be identified and notified.  On gitlab.com please ping a developer since it
may not be actively monitored.

## Prerequisites

We try to keep jetto-pythontools modular and easy-to-install. However, to
keep our sanity, we request at least a recent version of:
- `python >= 3.7.0`
- `pip >= 20.0.0 `

Different scripts might require different dependecies. Whenever a module is
missing, not provided by the default environment of the machine you are at, 
and not installed by our `pip install` process, please open an issue. 

## Installation (user)

Install the [latest relase from PyPi](https://pypi.org/project/jetto-tools/), 
including the plotting GUI `jpyplot`

```
sudo apt-get install python3-tk idle3  # On Ubuntu, tk is not always installed
sudo pip install jetto-tools[gui,tests]
```

Or for a lightweight install without the plotting GUI

```pip install jetto-tools```


## Installation (developer)

An easy way to get up and running is to install from the git repository in developer mode.

``` bash
python --version # Make sure you have at least python3.7
pip --version # Make sure you have at least version 20.0 of pip to read pyproject.toml files
git clone git@git.ccfe.ac.uk:jintrac/jetto-pythontools.git # Clone from JET repository if you have access
# Or git clone https://gitlab.com/jintrac/jetto-pythontools.git # for the public version
pip install -e jetto-pythontools
python -c "import jetto_tools; print(jetto_tools.__version__)" # Check if you indeed installed the right version and can call it in python
```

However, on Heimdall / Freia, editable mode does not always work, unless pip is updated.  For Freia testing of GUI changes, use
```
module unload jintrac-pythontools
pip install --user --upgrade pip
cd jetto-pythontools
python -m pip install --user -e .
python -m pip install --user -e .[gui,tests]  #GUI needs to be installed explicitly
```

In some cases, you might also need to 

```
export PATH=$HOME/.local/bin:$PATH
export PYTHONPATH=$HOME/.local/lib/python3.7/site-packages:$PYTHONPATH
```

to make your local install take precedence over the central installation.  (Note: in some versions of Python, local installs take precedence over the default installed version in PYTHONPATH (via importlib) - 
but this is not the case with the importlib in Python version 3.7.1 on Heimdall - hence the need for explicit PYTHONPATH modification).  

You can then launch the scripts or gui of your local install directly from PATH e.g. `jpyplot`.


### Non-pip builds (e.g. pure setuptools)
It is possible to build and install this package with other tool. In that case,
make sure your tools can read `pyproject.toml` files, and be able to generate
a version number somehow. For setuptools, that means:
- `setuptools >=40.8.0`
- `setuptools_scm[toml]>=3.4`

### Developer notes
- Do not add JET or other tokamak data to this repository! This repository is synced to
an open gitlab repository on [gitlab.com](https://gitlab.com/jintrac/jetto-pythontools)
- Open Issues and MRs at JET if you have access, or on gitlab.com if you don't.  On gitlab.com please ping a developer since it
may not be actively monitored.
- We try to follow the Python Package Authority recommendations. A full guide to
install Python packages can be found [on their website](https://packaging.python.org/tutorials/installing-packages/)
- In some cases the editable install does not pickup changes (?), in which case prepending the working dir to PYTHONPATH can be a workaround - See [Editable install requires python/3.7.9](https://git.ccfe.ac.uk/jintrac/jetto-pythontools/-/issues/13) (not yet in Heimdall site packages so you would need a venv for this)
- If you are making more major changes, you may prefer to use a venv, following the [expert install procedure](https://git.ccfe.ac.uk/jintrac/jetto-pythontools/-/issues/11)


## Features and Examples

### JETTO scan API

To progamatically generate JETTO runs from python, most useful for scans.

* See [API docs](https://jintrac.gitlab.io/jetto-pythontools/) deployed on gitlab pages

### JETTO plotting GUI

The `jpyplot` tool allows to load and plot runs from either the command line or a GUI. 
If you launch it from a run directory it loads that case automatically.

Particularly useful is to specify run dirs and plot variables from the CLI e.g.

```
jpyplot --plotvars=TI,TE,NE run1 run1 runwild*
```

* [Overview of jpyplot design](https://users.euro-fusion.org/pages/data-cmg/wiki/files/JETTO_plotting_jpyplot.pdf) also [here](https://gitlab.com/jintrac/jetto-pythontools/-/wikis/uploads/464fed7e9385aaf865716787448085ba/JETTO_plotting_jpyplot.pdf)
* See [this comment](https://git.ccfe.ac.uk/jintrac/jetto-pythontools/-/merge_requests/17#note_79461) to change default linestyles

### JETTO binary tools

The binary tools (in `jetto_tools/binary.py`) reads native JETTO outputs and can write JETTO inputs (exfiles)

* `convert_binary_file(input_file,output_file)`:    Converts .ex,.ext,.jsp,.jst,.jse files into ASCII equivalent for easy reading
* `read_binary_file(input_file)`:                   Reads .ex,.ext,.jsp,.jst,.jse files into memory (specific structure) for further processing in Python
* `write_binary_exfile(data,output_file)`:          Writes data (specific structure) into binary file according to .ex format
* `modify_entry(data,key,moddata)`:                 Modifies entry under key in data (specific structure), replacing it with moddata and updating tracking

One use is to read an existing ex-file into memory to
generate the specific structure needed, modifying it as required using
the function as it preserves some degree of providence, and writing it
back out as a binary for use in JETTO. The tracking is updated simply by
erasing all DDA/DTYPE/SEQ tags and replacing the DDA tag with the string
"Python modification tool" and setting seq=0.

**Simple example** to expose what the low level functions do (don't actually make plots like this, use the JETTO class - see below...!):

```
from jetto_tools.binary import *
import matplotlib.pyplot as plt

jst = read_binary_file('jetto.jst')
time = jst['TVEC1'][0,:] # First index is rho-index,
                         # but since this is a time trace,
                         # dimension is singular
Teax = jst['TEAX'][0,:]

plt.figure()
plt.plot(time,Teax,label='Simulation')
plt.legend()
plt.xlabel('Time [s]')
plt.ylabel('Te,core [eV]')
plt.show()

```

### JETTO class

The JETTO class reads all data into a structure which drives the results_gui (`jpyplot`).

For more information:

* Overview of class design [here](https://gitlab.com/jintrac/jetto-pythontools/-/wikis/uploads/464fed7e9385aaf865716787448085ba/JETTO_plotting_jpyplot.pdf)
* Try using the docstrings...
* Try browsing or searching the gitlab [issues](https://git.ccfe.ac.uk/jintrac/jetto-pythontools/-/issues) and merge requests.

**Example** (cut down from [here](https://git.ccfe.ac.uk/jintrac/jetto-pythontools/-/merge_requests/21)) - untested...

```
from pathlib import Path

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

from jetto_tools.classes import JETTO, ODS
from jetto_tools.results_gui import run_list_to_runs, slice_plotter

from IPython import embed

# Read runs
run_list = ['run1','run2']
runs = run_list_to_runs(run_list)

# For convenience, extract a JINTRAC run
jrun = runs[list(runs.keys())[0]]
jsp = jrun['JSP']

# Set plot variables
yvar = 'TE'
file = 'JSP'
# Find the max time in all JSPs
max_time = np.max([run[file]['time'].max() for run in runs.values()])
time = max_time

# Use GUI scripts to make a plot
fig, axes = plt.subplots(3)
ax0, ax1, ax2 = axes
xvar = 'XRHO'
for ax, yvar in zip(axes, ['TE', 'TI', 'NE']):
    slice_plotter(ax, None, runs, file, xvar, yvar, zslice=('time', time), verbosity=1)

ax0.legend([Path(k).name for k in runs.keys()])
plt.show()
```

## Adding Documentation

Some external user docs are maintained on the JINTRAC pages (WIP: merging here):
* https://users.euro-fusion.org/pages/data-cmg/wiki/JETTO_python_tool.html

Developer API docs are deployed on gitlab pages via gitlab CI:
* https://jintrac.gitlab.io/jetto-pythontools/

The API documentation is written using reStructuredText and Sphinx. In order to build the 
documentation, run the commands:

```
$ cd docs/
$ make html
```
They can then be viewed in the browser of your choice e.g.
```
$ firefox docs/_build/html/index.html
```
The packages required to build the documentation are listed in `requirements_docs.txt`.
If this pakage was installed via `pip`, as above, then the prerequisites should have
been installed automatically.
