#!/bin/bash

makeblastdb -in "$1" -parse_seqids -dbtype "$2" -out "$3" -title "$4"
