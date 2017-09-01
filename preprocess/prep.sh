#!/bin/bash

set -e
set -o pipefail

PREPROCESS_DIR="preprocess"
python=python3

detok=${PREPROCESS_DIR}/scripts/moses_r3_detokenizer.perl
tok=${PREPROCESS_DIR}/scripts/moses_r3_tokenizer.perl
apply_bpe=${PREPROCESS_DIR}/scripts/apply_bpe.py


while [[ $# -gt 1 ]]
do
key="$1"

case $key in
    -l|--lang)
    LANG="$2"
    shift
    ;;
    -f|--file)
    FILE="$2"
    shift
    ;;
    *)
      # unknown option
    ;;
esac
shift
done

bpe_codes=${PREPROCESS_DIR}/bpe/UNv1.0.6way.${LANG}.apos.tok.lc.codes20k
zcat ${FILE} \
   | ${detok} -q -no-escape -threads 28 -l ${LANG} \
   | sed -f ${PREPROCESS_DIR}/scripts/tokenizers/correct_tok_${LANG}.sed -e 's/can not/cannot/g' \
   | ${tok} -q -no-escape -threads 28 -l ${LANG} \
   | awk '{print tolower($0) }' \
   | $python ${apply_bpe} -c ${bpe_codes}
