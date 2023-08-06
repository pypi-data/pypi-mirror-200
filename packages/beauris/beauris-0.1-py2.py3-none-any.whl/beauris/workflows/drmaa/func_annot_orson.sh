#!/bin/bash

nextflow run $ORSON_PATH/main.nf \
  --fasta $1 \
  --query_type p \
  --downloadDB_enable false \
  --busco_enable false \
  --beedeem_annot_enable true \
  --hit_tool diamond \
  --blast_db $BLAST_DB_PATH \
  -profile custom,singularity \
  --chunk_size 200 \
  -c $CLUSTER_CONFIG_PATH \
  --outdir ./results \
  -w $SCRATCH_WORK_DIR \
  --projectName func_annot_orson \
  -ansi-log false \
  -resume \
  $2