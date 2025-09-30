#!/bin/bash
# This shell script basically will set up a virtual environment and the pip requirements
basedir=$(dirname $(realpath $0))
if [ $# -gt 1 ]; then
  fulldirpath=$1
  venvbase=$(dirname $fulldirpath)
else
  venvbase=~/virtual_environments
  fulldirpath="${venvbase}/${basedir##/*/}"
fi

if [ -e "${fulldirpath}/bin/activate" ]; then
  if [ ! -e "${basedir}/.venvlocation" ]; then
    echo $fulldirpath > ${basedir}/.venvlocation && \
    echo "Created ${basedir}/.venvlocation"
  fi
  echo "Virtual Environment already made, checking pip and will install packages if needed.."
  bash -c \
    "source ${fulldirpath}/bin/activate; \
     pip freeze > ${basedir}/test.txt; \
     diff ${basedir}/test.txt ${basedir}/requirements.txt || \
     pip install -r ${basedir}/requirements.txt; \
     rm ${basedir}/test.txt"
else
  if [ ! -d "$venvbase" ]; then
    mkdir -p "$venvbase" && echo "Created Virtual Enviornments Base Dir: $venvbase"
  fi
  echo "Creating virtual environment in the following directory $fulldirpath"
  # Get the python3 binary
  python=$(which python3)
  if [ -z "$python" ]; then
    echo "Python3 not found, exiting"
    exit
  fi
  
  bash -c "$python -m venv $fulldirpath"
  echo $fulldirpath > ${basedir}/.venvlocation
  bash -c "source ${fulldirpath}/bin/activate && pip install -U pip && pip install -r ${basedir}/requirements.txt"
fi

echo "Virtual Environment setup completed. Run './venv_shell' to switch to Virtual Environment sub shell"