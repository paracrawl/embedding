#!/bin/bash

# Normalize script
# set -x
function usage {
    echo "usage: $(basename $0) <filename> <source> <target> <min> <max> <output>\n"
    echo "example: $0 eparl7.fr-es-en en es 1 50 output.txt"
    exit 1
}

MOSES_PATH=/mt/mosesdecoder
MOSES_LOWER_SCRIPT="$MOSES_PATH/scripts/tokenizer/lowercase.perl"
MOSES_TOKENIZER_SCRIPT="$MOSES_PATH/scripts/tokenizer/tokenizer.perl"
MOSES_CLEAN_CURPOS_SCRIPT="$MOSES_PATH/scripts/training/clean-corpus-n.perl"


if [ ! -z ${MOSES_PROGRAM} ]; then
  MOSES_PATH=$MOSES_PROGRAM
fi

if [ ! -d ${MOSES_PATH} ];then
   echo "Please set your MOSES_PROGRAM environment variable first!"
   exit
fi



if [ "$#" -ne 6 ];then
   usage
fi

if [ ! -f "$1.$2.gz" ]; then
  echo "Sorry, but we can't encounter the file: $1.$2.gz"
  exit 3
fi

name_of_input_file=$1
name_of_source_language=$2
name_of_target_language=$3
min=$4
max=$5
name_of_output_file=$6

zcat ${name_of_input_file}.${name_of_source_language}.gz | sort |${MOSES_LOWER_SCRIPT} > "./.lower.${name_of_source_language}"
${MOSES_TOKENIZER_SCRIPT} < "./.lower.${name_of_source_language}" > "./.tokenized.${name_of_source_language}"

zcat ${name_of_input_file}.${name_of_target_language}.gz | sort |${MOSES_LOWER_SCRIPT} > "./.lower.${name_of_target_language}"
${MOSES_TOKENIZER_SCRIPT} < "./.lower.${name_of_target_language}" > "./.tokenized.${name_of_target_language}"


${MOSES_CLEAN_CURPOS_SCRIPT} "./.tokenized" ${name_of_source_language} ${name_of_target_language} ${name_of_output_file} ${min} ${max}


if [ $? -ne 0 ]; then
   echo "Something bad happened"
fi


