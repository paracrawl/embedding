#!/bin/bash

#
# This scripts downloads the file from the url sent as first argument and uploads it
# to Azure Blob Storage. A named pipe is used in order to not have the file written
# directly into the machine.
#

ACCOUNT_NAME="mtmaccount"
CONTAINER_NAME="mtmblob"
FIFO_NAME="toBlobFifo"
URL=$1
FILE_NAME_ON_BSTORAGE=$2
FIFO_NAME="$FIFO_NAME$FILE_NAME_ON_BSTORAGE"


# validate parameters
if [ "$#" -ne 2 ]
then
  echo "Please insert two arguments: "
  echo "#1: URL"
  echo "#2: File name in Blob Storage"
  exit 1
fi



# create the named pipe/fifo
`mkfifo $FIFO_NAME`
echo "Named pipe created."


# uploads the file to Blob Storage when it is written into the named pipe and deletes it at the end
az storage blob upload --container-name $CONTAINER_NAME --file $FIFO_NAME --name $FILE_NAME_ON_BSTORAGE --account-name $ACCOUNT_NAME && rm $FIFO_NAME &
echo "Uploading from the named pipe."


# downloads the file from the URL and sends it to the fifo 
wget -qO- --no-check-certificate --no-proxy $URL > $FIFO_NAME &
echo "Downloading the file in background and sending it to the named pipe."
