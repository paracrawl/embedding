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
MOSES_TOKENIZER_SCRIPT="/data/holger/europarl.un16lc/tools/moses_r3_tokenizer.perl"
MOSES_CLEAN_CURPOS_SCRIPT="$MOSES_PATH/scripts/training/clean-corpus-n.perl"

SUBWORD_PATH=../subword-nmt
SUBWORD_BPE="$SUBWORD_PATH/apply_bpe.py"

BPE_CODES=/data/holger/europarl.un16lc/bpe

if [ ! -z ${MOSES_PROGRAM} ]; then
  MOSES_PATH=$MOSES_PROGRAM
fi

if [ -f /proc/cpuinfo ]; then
  CPUS=$(grep flags /proc/cpuinfo |wc -l)
elif [ ! -z $(which sysctl) ]; then
  CPUS=$(sysctl -n hw.ncpu)
else
  CPUS=2
fi

if [ ! -d ${MOSES_PATH} ];then
   echo "Please set your MOSES_PROGRAM environment variable first!"
   exit
fi

if [ "$#" -ne 6 ];then
   usage
fi

if [ ! -d ${SUBWORD_PATH} ]; then
  echo "Sorry, but we can't encounter the subword directory"
  exit 3
fi

name_of_input_file=$1
name_of_source_language=$2
name_of_target_language=$3
min=$4
max=$5
name_of_output_file=$6

#Source lang
zcat ${name_of_input_file}.${name_of_source_language}.gz \
| ${MOSES_LOWER_SCRIPT} > "./.lower.${name_of_source_language}"

${MOSES_TOKENIZER_SCRIPT} -no-escape -threads ${CPUS} < "./.lower.${name_of_source_language}" > "./.tokenized.${name_of_source_language}"

#Target lang
zcat ${name_of_input_file}.${name_of_target_language}.gz \
| ${MOSES_LOWER_SCRIPT} > "./.lower.${name_of_target_language}"

${MOSES_TOKENIZER_SCRIPT} -no-escape -threads ${CPUS} < "./.lower.${name_of_target_language}" > "./.tokenized.${name_of_target_language}"

#Source lang
gunzip -c "${BPE_CODES}/UNv1.0.6way.${name_of_source_language}.apos.tok.lc.codes20k.gz" > "/tmp/${name_of_source_language}"

cat "./.tokenized.${name_of_source_language}" \
| python ${SUBWORD_BPE} -c "/tmp/${name_of_source_language}" > "./.bpe.${name_of_source_language}"

#Target lang
gunzip -c "${BPE_CODES}/UNv1.0.6way.${name_of_target_language}.apos.tok.lc.codes20k.gz" > "/tmp/${name_of_target_language}"

cat "./.tokenized.${name_of_target_language}" \
| python ${SUBWORD_BPE} -c "/tmp/${name_of_target_language}" > "./.bpe.${name_of_target_language}"

#Clean
${MOSES_CLEAN_CURPOS_SCRIPT} "./.bpe" ${name_of_source_language} ${name_of_target_language} ${name_of_output_file} ${min} ${max}

paste -d"|" "${name_of_output_file}.${name_of_source_language}" "${name_of_output_file}.${name_of_target_language}" \
| sort | uniq -u > ./.out

cut -d"|" -f1 ./.out  > "${name_of_output_file}.${name_of_source_language}"
cut -d"|" -f2 ./.out  > "${name_of_output_file}.${name_of_target_language}"

rm ./.*
