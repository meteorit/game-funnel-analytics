# Project README

**Author**: Sampsa Rannala (sampsa.rannala@gmail.com)

## Project Folder structure

- project root
    * this README file, conda environment YML, solution documentation

- notebooks
    * Notebooks with solutions to questions 1 & 2

- db
    * SQLite database

- reports
    * Static reports in HTML format (for code & cell outputs & ToC,  open the HTML files inside Table of Contents-enabled subfolders. Reports folder also contains single-HTML files with notebook output only)

- raw data sources
    * Project datasets

- lib
    * All Python code written for project - both backend and jupyter notebook code

## Static Reports

 Exported HTML output of notebooks can be found in reports folder. These have no interactivity but otherwise represent the notebooks' contents faithfully. Versions with input cells (code) only, output cells only, and all cells are provided.

 If you wish to view the interactive jupyter notebooks and optionally set up a virtual conda environment, please follow the instructions below.

## Interactive Jupyter Notebooks

Only requirement to open and view the project ipynb-files is to have python and jupyter notebook package installed on your system. But if you intend to execute code cells, it becomes necessary to have all the dependencies installed. For this purpose I have provided environment.yml file to easily deploy a conda virtual environment.

## Virtual Environment Installation

This environment will have all the required dependencies to run the code in project notebooks - as well as the modules contained in lib folder.

### Conda package manager install

Prerequisites: Conda package manager installed on your system.
See https://conda.io/docs/installation.html for instructions.

#### Deploy Virtual Environment

Navigate to project root in command line after you have installed conda to system Path.

- Create conda environment

        conda env create -f environment.yml

- Activate conda environment

        conda activate rannala_project

    or if that does not work try

        source activate rannala_project

#### Launching Jupyter Notebooks

We can launch Jupyter Notebook browser session from the command line.

First make sure that you are in either project root or /notebooks folder, and that rannala_project virtual environment is active. Then run:

        jupyter notebook

That's it! A new browser tab with project folder contents should open up in a few seconds. Open a notebook (navigate to /notebooks folder if not there already) to view and interact with the contents.

#### Launching JupyterLab (alternative frontend)

Altair rendering used for visualization actually prefers JupyterLab frontend. But in this project I mainly worked in Jupyter Notebook and enabled settings to support it. There is one line of code to comment out if you choose to execute notebook code cells with JupyterLab (see the last row of this document for details).

To start a JupyterLab browser session from the command line:

- Again, make sure you are in either project root or /notebooks folder, and that rannala_project virtual environment is active. Then run:

        jupyter lab

A new browser tab should open up. Choose a notebook for viewing and interacting with the contents. After opening the notebook, if you intend to execute code cells, make sure that the following import line is **commented out**:

    # alt.renderers.enable('notebook')