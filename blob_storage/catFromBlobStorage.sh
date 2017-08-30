#!/bin/bash

#
# This scripts downloads the file from the Blob storage server and displays it
# in the stdout, like the cat command. A named pipe is used in order not to have 
# the file written directly into the machine.
#

ACCOUNT_NAME="mtmaccount"
CONTAINER_NAME="mtmblob"
FIFO_NAME="blobStorageCat"
FILE_NAME_ON_BSTORAGE=$1
FIFO_NAME="$FIFO_NAME$FILE_NAME_ON_BSTORAGE"


# validate parameters
if [ "$#" -ne 1 ]
then
  echo "Please insert one argument: file name on Blob Storage. "
  exit 1
fi

# create the named pipe/fifo
`mkfifo $FIFO_NAME`

# downloads the specified file from the blob storage and sends it into the fifo
az storage blob download --container-name $CONTAINER_NAME --name $FILE_NAME_ON_BSTORAGE --file $FIFO_NAME --output table --account-name $ACCOUNT_NAME > /dev/null &


# displays the content from the fifo and deletes it at the end
cat | xz -d < $FIFO_NAME && rm $FIFO_NAME
