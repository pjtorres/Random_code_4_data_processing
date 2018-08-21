#!/bin/bash

#collect seqids for taxa of interest

taxa=$1

echo "$1" 

grep "$1"  taxonomy/names.dmp | cut -d'|' -f1| sort | uniq

#example
#./get_taxid.sh 'Alistipes shahii'
#group analyis 
# while read line; do ./get_taxid.sh "${line%}"; done <test.txt
