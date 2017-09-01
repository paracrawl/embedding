#!/bin/bash

PREPROCESS_DIR="preprocess"

clean_copus=${PREPROCESS_DIR}/scripts/moses_clean-corpus-n.perl


# $1 file withouth lang extension
# $2 lang source
# $3 lang target
# $4 name of the output file
# $5 min
# $6 max
#Example input en es output 5 50 produces output.en and ouput.es
${clean_copus} $1 $2 $3 $4 $5 $6

#Merge - sort - remove duplicates
paste -d"|" "$4.$2" "$4.$3" \
| sort | uniq -u
#| cut -d"|" -f1 
 



