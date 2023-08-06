# MAPHIS
https://cbia.fi.muni.cz/software/maphis.html
## Outline
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running](#running)
4. [User guide](#user-guide)

## Prerequisites
`MAPHIS` is currently compatible only with `Python 3.8`. In this guide we'll detail how to obtain `Python 3.8` and create a Python virtual environment using `miniconda` (https://docs.conda.io/en/latest/miniconda.html). 
Other ways of obtaining `Python 3.8` include downloading it from (https://www.python.org/downloads/) or using `pyenv` (https://github.com/pyenv/pyenv). Virtual environment management can be also achieved with the modules `venv` (https://docs.python.org/3/library/venv.html) or `virtualenv` (https://virtualenv.pypa.io/en/latest/).

### Set up Python 3.8 and virtual environment
1. Download and install `miniconda` for your operating system from: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

2. Open up `Anaconda Powershell Prompt` or `Anaconda Prompt` (Windows) or your terminal emulator (Linux/Mac)

3. Create a new virtual environment called `maphis` with `Python 3.8` as its interpreter: `conda create -n maphis python=3.8`

## Installation

### Installation from `pip`
  1. Activate the virtual environment: `conda activate maphis`
  2. Install the app: `python -m pip install maphis`

#### Running
  1. Activate the virtual environment: `conda activate maphis`
  2. Run as: `python -m maphis`

### Installation from the repository (developer purposes)

1. Clone this repository
2. Go to the root directory of the cloned repository
3. Activate the virtual environment: `conda activate maphis`
4. Install the requirements: `python -m pip install -r requirements.txt`
5. Install the app: `python -m pip install -e .`
   
#### Running from the repository

1. Activate the virtual environment: `conda activate maphis`
3. Go to the root directory of the cloned repository
2. Run: `python maphis/__main__.py`

## User guide
The user guide is located at: https://cbia.fi.muni.cz/software/maphis.html