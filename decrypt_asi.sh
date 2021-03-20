#!/bin/bash


filename=$1

output=${filename%%.c}

timeStamp=${filename%%.tar.gz.c}
timeStamp=${timeStamp##*ASILog.}
passPhrase=ASILogAV1C1I${timeStamp}


gpg --ignore-mdc-error --batch --passphrase ${passPhrase} -o ${output} -d ${filename}

mkdir ${filename%/*}

