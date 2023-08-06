#!/bin/bash

ln -s "$1" input.bam
ln -s "$2" input.bai
ln -s "$3" genome.fa

bedtools genomecov -split -ibam input.bam -bg > output.bg

bedSort output.bg output.bg.sorted

samtools faidx genome.fa -o genome.fa.fai

bedGraphToBigWig output.bg.sorted genome.fa.fai "$4"
