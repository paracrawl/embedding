#!/bin/bash

# Normalize script

#set -x

moses_directory=/mt/mosesdecoder
moses_lower_case_script="$moses_directory/scripts/tokenizer/lowercase.perl"
moses_tokenizer_script="$moses_directory/scripts/tokenizer/tokenizer.perl"
moses_clean_cupos="$moses_directory"

if [ ! -z ${MOSES_PROGRAM} ]; then
  moses_directory=$MOSES_PROGRAM
fi

if [ ! -d ${moses_directory} ];then
   echo "Moses program not found"
   exit 1
fi

if [ "$#" -ne 2 ];then
  echo "Usage: $0 nameOfInputFile nameOfOutputFile"
  exit 2
fi

if [ ! -f $1 ]; then
  echo "Sorry, but we can't encounter the file!"
  exit 3
fi

name_of_input_file=$1
name_of_output_file=$2

zcat ${name_of_input_file} | sort | ${moses_lower_case_script} | ${moses_tokenizer_script} > ${name_of_output_file}.$3 $3 
 
if [ $? -ne 0 ]; then
   echo "Something bad happened"
fi
