#!/bin/bash

#ASK for sequence depth

FASTQ=$1
seqdepth=$2
a=$((4*$seqdepth))

echo for the  $FASTQ file you want to get the top $seqdepth fastq files which will equal $a lines

cat $FASTQ | head -n $a >> ${FASTQ%.fastq}_$seqdepth.fastq

#./split.sh <fastq file> <n number of lines>
