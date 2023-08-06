# ACES Applications (aces-apps)
ASKAP Comissioning and Early Science python packages.

## Provides:
A collection of tools developed by members of the ACES team to support ACES processing:
* `aces.askapdata` - Tools for retrieving ASKAP observation metadata including:
  * scheduling block info
* `aces.beamset` - beamset classes supporting beam analysis
* `aces.cleanlog` - Tools for analysing imager deconvolution (clean) logs
* `aces.data` - Antenna positions.
* `aces.display` - Tools for displaying data summaries
* `aces.fov` - Tools for field-of-view modelling
* `aces.holography` - Tools for processing holography data to measure beams:
  * Extract a holography beamset from an ASKAP measurement set
* `aces.misc` - Tools miscellaneous tasks
* `aces.mpfit` - Perform Levenberg-Marquardt least-squares minimization.
  * The original version of this software, called LMFIT, was written in FORTRAN as part of the MINPACK-1 package.
* `aces.obsplan` - Tools for planning ASKAP observations including:
  * Footprint utilities
* `aces.sefd` - Tools for estimating ASKAP sensitivity
  * SEFD from 1934 data
* `aces.survey` - Tools for processing ASKAP survey data


## Installation

Below are some instructions that attempt to outline the way to install for most situations.

The primary dependencies and build instructions for `pip` are located in `pyproject.toml`.

Currently, the installation depency for the `askap` module is defined in `askap-requirements.txt`.

### 'I just want it deployed'

This is intended if you just want to install the tooling in a modular and simple fashion.

NOTE: You'll need to [install conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) on your system first.


```bash
# If using ssh:
git clone ssh://git@bitbucket.csiro.au:7999/aces/aces-apps.git

# If using https:
git clone https://bitbucket.csiro.au/scm/aces/aces-apps.git

cd aces-apps
# Optional: Checkout a specific version of aces-apps. By default, this will be the latest (`master`) version.
git checkout {VERSION}

# Create a conda environment with optional name. If you don't specify a name (with -n {ENVIRONMENTNAME}), it will be called 'aces'
conda env create -n {ENVIRONMENTNAME}

# Activate the environment
conda activate {ENVIRONMENTNAME}
```

Please note though that `VERSION` and `ENVIRONMENTNAME` are simply placeholders and need to be updated appropriately.

In the above, the following occurs:
* The repository is cloned into a new directory (using `ssh` or `https`)
* A desired version is optionally checked out
* A `conda` environment is created installing the software.


NOTE: If you have any error around `mpi4py` on a Pawsey system such as `galaxy`, see the section below that outlines the modules that need to be loaded.

### Slightly more advanced
This outlines a process that gives a little more granularity for bespoke processes and use cases. Installing `aces-apps` should be a fairly straightforward process.

The current version (`1.3.0`) expects a python 3.9 installation. It is recommended that a `conda` virtual environment is created with this version:

```bash
conda create -n {ENVIRONMENTNAME} python=3.9 -y
```

This will create a new conda environment with the appropriate python version installed.

Next, activate this environment with

```bash
conda activate {ENVIRONMENTNAME}
```

Before issuing the next set of `pip` commands, please first take note whether you will be installing this package on a system with specialised MPI tooling. For example, Cray style HPC. If so, refer to the next section.

Once the `conda` environment you previously installed has been activated (and the `mpi` tooling requirements have been dealt with), install `aces-apps` should be straight-forward.

```bash
# If using ssh:
pip install git+ssh://git@bitbucket.csiro.au:7999/aces/aces-apps.git@1.3.0

# If using https:
pip install git+https://bitbucket.csiro.au/scm/aces/aces-apps.git@1.3.0
```

This command should clone the `aces-apps` repository to a temporary space, checkout the `1.3.0` tag, and use the `pyproject.toml` file to identify dependencies, and their version specifications. *Please note the @1.3.0 tag* which will install a specific version of the `aces-apps` tooling.

If an `mpi4py` compilation error is thrown, the required `mpi` libraries and environments are likely not correctly defined. Please refer to the next section if using Galaxy/Pawsey, or the documentation for your HPC system.

Finally, the `askap` python module needs to be installed (or rather, a subset of the complete module). This is being performed as a final step as its current layout is not well suited for automated installation with typical tooling. Issue these these commands:

```bash
pip install -r requirements.txt

# - OR -

pip install git+https://bitbucket.csiro.au/scm/tos/python-askap.git#egg=askap
pip install git+https://bitbucket.csiro.au/scm/tos/python-parset.git#egg=askap.parset
pip install git+https://bitbucket.csiro.au/scm/tos/python-footprint.git#egg=askap.footprint
```

Specifically, the `python-askap` module is actually a small set of independent modules. The above set of `pip` commands will install each module instal a common namespace as a submodule. The use of the `egg=askap` argument in the endpoint is important. If a specific version of `python-askap` is required this will need be set using the typical `@1.2` style of notation.

### Installing as a developer

If you are trying to develop or test code as part of the `aces-apps` tooling, the above instructions are mostly correct, but some slight tweaks are needed.

First, clone the repository and checkout the appropriate tag/branch.

```bash
# If using ssh:
git clone ssh://git@bitbucket.csiro.au:7999/aces/aces-apps.git

# If using https:
git clone https://bitbucket.csiro.au/scm/aces/aces-apps.git

cd aces-apps
git checkout {VERSION}
```

If you are planning on developing a new feature it is also recommended that a new branch is created to isolate changes from the main.

Then create the `conda` environment and activate it

```bash
conda create -n {DEV_ENVIRONMENTNAME} python=3.9
conda activate {DEV_ENVIRONMENTNAME}
```

Unlike the previous set of `conda` environment commands, this one *will not* use the `environment.yml` file to auto magically install everything.

Provided the above has worked, you can then do a _developer install_ of the `aces-apps` by

```bash
pip install -e .
```

The `-e` will essentially create a symlink from the `site-packages/aces` path to the current location. This will let you edit code from the current location and be picked up when running scripts that `import aces`.

Finally, configure the `askap` tooling.

```bash
pip install -r requirements.txt

# - OR -

pip install git+https://bitbucket.csiro.au/scm/tos/python-askap.git#egg=askap
pip install git+https://bitbucket.csiro.au/scm/tos/python-parset.git#egg=askap.parset
pip install git+https://bitbucket.csiro.au/scm/tos/python-footprint.git#egg=askap.footprint
```

### Notes on `mpi4py`
Some tooling in `aces-apps` repositories relies on `mpi` for code parallelism. On some cray-type supercomputing systems this requires a specialised set of `mpi` libraries and compilers. The `galaxy` system is such a machine. This tooling needs to be loaded into the shell environment before issuing the `pip` command to install `aces-apps`. On Galaxy, issue these commands:

```bash
# Extra environment commands for galaxy
module swap PrgEnv-cray PrgEnv-gnu
export MPICC=/opt/cray/pe/craype/2.5.13/bin/cc
```

Similarly, on `zeus` the following commands are required:

```bash
# Extra environment commands for zeus
module load intel-mpi
export MPICC=/pawsey/intel/17.0.5/compilers_and_libraries/linux/mpi/intel64/bin/mpicc
```

These can be combined, and placed into your `~/.bashrc`:
```bash
# MPI4PY
# Test if machine is galaxy
machine=$(hostname)
if [[ $machine == galaxy* ]]; then
    module swap PrgEnv-cray PrgEnv-gnu
    export MPICC=/opt/cray/pe/craype/2.5.13/bin/cc
fi

# test if machine is zeus
if [[ $machine == zeus* ]]; then
    module load intel-mpi
    export MPICC=/pawsey/intel/17.0.5/compilers_and_libraries/linux/mpi/intel64/bin/mpicc
fi
```

Please note that these instructions may not be correct or relevant on other HPC machines, including others at Pawsey. Care will need to be taken if attempting to deploy the package on a Cray style system.

A sample script `aces_test_mpi_install.py` is installed alongside this package as a way of verifying an `mpi` installation and configuration should it be needed.


## Notes from mpfit

_Taken verbatim from the mpfit documentation_

This library contains a few useful routines I wrote or I converted from IDL.

My contacts are:
Sergey Koposov koposov@ast.cam.ac.uk
Institute of Astronomy, University of Cambridge
Madingley road, CB3 0HA, Cambridge, UK

If you have found a bug or have a patch, you can send them to me.
With my library I do not promise a stable interface, so beware.

The licensing for the programs I wrote myself is GPL3. For all other
programs (mainly converted from IDL) I guess the license is either BSD or
they are in public domain.

Here is the quick list of the functions I implemented:
TBW
