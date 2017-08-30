#!/bin/bash

# ======================================================================================================
# This script is intended to loop through all the files in http://data.statmt.org/ngrams/deduped_en/ and
# download it to an azure blob storage.
# ======================================================================================================

ZERO="0"
urlhead="http://web-language-models.s3-website-us-east-1.amazonaws.com/ngrams/en/deduped/en."
urltail=".deduped.xz"
language="en."

for i in {0..99}
do
        if [[ $i =~ ^[0-9]$ ]]; then
                name=$ZERO$i
        else
                name=$i
        fi
	finalurl=$urlhead$name$urltail
        echo "File to download: $finalurl"
	sh uploadToBlobStorage $finalurl $language$name
done
