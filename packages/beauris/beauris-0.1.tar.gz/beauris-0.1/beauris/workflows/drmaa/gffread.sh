#!/bin/bash

name="$3"
gffread $1 -g $2 -w ${name}_transcripts_raw.fa -y ${name}_proteins_raw.fa -x ${name}_cds_raw.fa -S

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

echo "Renaming fasta sequences with command:"
echo python "$SCRIPT_DIR/gffread_fa_rename.py" $4 ${name}

python "$SCRIPT_DIR/gffread_fa_rename.py" $4 ${name}
