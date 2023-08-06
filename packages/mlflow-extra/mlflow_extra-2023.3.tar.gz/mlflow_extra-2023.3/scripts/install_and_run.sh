#!/usr/bin/env bash
set -euo pipefail

function show_help()
{
  cat << HELP
SYNOPSIS

  Run a command from the MLflow Extra package. The command will be installed in
  a virtual environment if necessary.

USAGE
  
  ${0##*/} <command> [args]

EXAMPLE

  ${0##*/} mlflow-fix_artifacts ./mlruns
HELP
}

cmd=("$@")

if [[ ${#cmd[@]} == 0 || ${cmd[0]:0:7} != 'mlflow-' ]]
then
  show_help
  exit 1
fi

# Install MLflow Extra in a virtual environment if necessary.
if ! command -v "${cmd[0]}" >/dev/null 2>&1
then
  # Clone the MLflow Extra repo if necessary.
  if [[ ! -d mlflow-extra ]]
  then
    git clone 'git@gitlab.inria.fr:jrye/mlflow-extra.git'
  fi

  mlflow-extra/scripts/install.sh -u venv
  source venv/bin/activate
fi

"${cmd[@]}"
