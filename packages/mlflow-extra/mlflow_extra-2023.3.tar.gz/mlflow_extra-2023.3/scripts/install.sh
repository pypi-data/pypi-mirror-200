#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}

function show_help()
{
  cat << HELP
SYNOPSIS

  Install the MLflow Extra package with pip.

USAGE

  ${0##*/} [-h] [-u] [path]

  "path" is an optional path to a virtual environment.

OPTIONS

  -h
    Show this help message and exit.

  -u
    Upgrade pip and the target package.
HELP
}

upgrade=false
while getopts 'hu' flag
do
  case "$flag" in
    u) upgrade=true ;;
    h) show_help 0 ;;
    *) show_help 1 ;;
  esac
done
shift $((OPTIND - 1))

if [[ -n ${1:+x} ]]
then
  venv_dir=$(readlink -f "$1")
  mkdir -p -- "$venv_dir"
  python3 -m venv "$venv_dir"
  source "$venv_dir/bin/activate"
fi

if $upgrade
then
  pip3 install --upgrade pip
fi
pip3 install --upgrade "$DIR"
