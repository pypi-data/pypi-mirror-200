#!/bin/bash

# Remove any pre-existing tmp and result dir
# Because at this stage we're sure we want to (re)run from scratch
rm -rf ./tmp ./results

python -u ~abretaud/func_annot/func_annot.py \
	-i $1 \
	-o ./results \
	-t ./tmp \
	-c 25 -j 25 \
	--keep-tmp \
	--diamond \
	--no-blast
