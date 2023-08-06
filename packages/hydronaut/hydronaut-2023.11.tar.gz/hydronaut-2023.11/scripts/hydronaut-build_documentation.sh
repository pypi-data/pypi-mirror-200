#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[0]}")
DIR=${SELF%/*/*}
DOC_DIR=$DIR/doc
SRC_DIR=$DIR/src

function show_help()
{
  cat << HELP
USAGE

  ${0##*/} [-i] [<directory>]

OPTIONS

  -i
    Install documentation dependencies with pip.

  <directory>
    An optional output directory for the generated files. If not given, they
    will be generated in a subdirectory named "public" in the current working
    directory.
HELP

  exit "$1"
}

install_deps=false
while getopts 'i' opt
do
  case "$opt" in
    i) install_deps=true ;;
    h) show_help 0 ;;
    *) show_help 1 ;;
  esac
done
shift $((OPTIND - 1))

output_dir=${1:-public}

if $install_deps
then
  pip install -r "$DOC_DIR/requirements.txt"
fi
sphinx-apidoc -o "$DOC_DIR/source" -f -H 'API Documentation' "$SRC_DIR"
mkdir -p "$output_dir"
sphinx-build -b html "$DOC_DIR/source" "$output_dir"
