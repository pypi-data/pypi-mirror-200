---
title: README
author: Jan-Michael Rye
---

# Synopsis

Provide several commands for working with MLflow output directories, such as merging experiments from separate mlruns directories into a single one or fixing artifact paths after moving an mlruns directory.

# Installation

Install the [MLflow Extra package](https://pypi.org/project/mlflow-extra) from the [Python Package Index](https://pypi.org/) using any standard Python package manager, e.g.

~~~sh
# Uncomment the following 2 lines to create and activate a virtual environment.
# python -m venv venv
# source venv/bin/activate
pip3 install --upgrade mlflow-extra
~~~

It can also be installed from source with any standard Python package manager that supports [pyproject.toml](https://peps.python.org/pep-0621/) files. For example, to install it with pip, either locally or in a virtual environment, run the following commands:

~~~sh
git clone https://gitlab.inria.fr/jrye/mlflow-extra
cd mlflow-extra
# Uncomment the following 2 lines to create and activate a virtual environment.
# python -m venv venv
# source venv/bin/activate
pip install --upgrade .
~~~

# Commands

These commands provide complimentary functionality for the [mlflow command-line interface](https://mlflow.org/docs/latest/cli.html).

## mlflow-filter_runs

A command-line tool to filter runs in an experiment using either metric threshold values or the total number of runs to keep.

~~~
$ mlflow-filter_runs --help
usage: mlflow-filter_runs [-h] [-a] [-c] [-l] [-m METRICS [METRICS ...]] [-n NUMBER] [-t THRESHOLDS [THRESHOLDS ...]] experiment_id

Delete runs from experiment based on thresholds.

positional arguments:
  experiment_id         The MLflow experiment ID (see mlflow experiments list).

options:
  -h, --help            show this help message and exit
  -a, --ascending       Keep the first n runs in ascending order instead of descending.
  -c, --confirm         Confirm the deletion. Without this only a dryrun is performed.
  -l, --list            List metrics and their statistics.
  -m METRICS [METRICS ...], --metrics METRICS [METRICS ...]
                        The metrics by which to filter runs.
  -n NUMBER, --number NUMBER
                        The number of runs to keep.
  -t THRESHOLDS [THRESHOLDS ...], --thresholds THRESHOLDS [THRESHOLDS ...]
                        The threshold values for the selected metrics. In descending order the threshold values are a lower limit. In ascending order they are an upper limit.
~~~

## mlflow-fix_artifacts

A command-line tool for fixing artifact URIs in experiment and run metadata files. It can be used to fix paths after they have been changed, either on the same system or when transferred from another.

~~~
$ mlflow-fix_artifacts --help
usage: mlflow-fix_artifacts [-h] [-m MAP] path

Attempt to fix broken artifact URIs in experiments and runs.

positional arguments:
  path               A path to a directory with experiments and runs.

options:
  -h, --help         show this help message and exit
  -m MAP, --map MAP  A path to a YAML file that maps old paths to new paths.
~~~

## mlflow-fix_experiment_ids

A command-line tool for fixing experiment IDs. The experiment ID will be set to the experiment's directory name if it is a non-negative integer (nni). If not, the directory will be renamed to the experiment's current ID if the ID is a nni, otherwise it will be renamed to the first available nni in the parent directory. The experiment ID will then be updated in the experiment and all runs in it.

~~~
$ mlflow-fix_experiment_ids --help
usage: mlflow-fix_experiment_ids [-h] paths [paths ...]

Attempt to fix experiment IDs so that the experiment's directory and all of its runs match its ID.

positional arguments:
  paths       Experiment directory paths.

options:
  -h, --help  show this help message and exit
~~~

## mlflow-merge

A command-line tool for merging experiments from multiple mlruns directories into a common directory. It will merge experiments with the same name and update experiment IDs to ensure consistency.

~~~
$ mlflow-merge --help
usage: mlflow-merge [-h] target dirs [dirs ...]

Copy experiments into a common MLflow directory. Runs from experiments with the same name will be merged.

positional arguments:
  target      The directory into which to merge the experiments. Default: None
  dirs        The directories with the experiments to merge.

options:
  -h, --help  show this help message and exit
~~~

# Python Module

See the [online documentation](https://jrye.gitlabpages.inria.fr/mlflow-extra/) for details.

# Utility Scripts

Several utility scripts are provided for convenience.

## install.sh

[install.sh](https://gitlab.inria.fr/jrye/mlflow-extra/-/blob/main/scripts/install.sh) will optionally set up a virtual environment and then install MLflow Extra from source with pip. See `install.sh -h` for details.

## install_and_run.sh

[install_and_run.sh](https://gitlab.inria.fr/jrye/mlflow-extra/-/blob/main/scripts/install_and_run.sh) will run any of the commands in the MLflow Extra package after ensuring that they are available by installing the package from source if necessary. It is useful for quickly fixing artifacts paths when transferring mlruns directories. See `install_and_run.sh -h` for details.
