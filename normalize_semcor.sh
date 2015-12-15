#!/bin/bash
if [ ! -d 'semcor3.0' ]; then
    echo 'No semcor install found! Attempting to download semcor3.0...'
    if ! curl -O http://web.eecs.umich.edu/~mihalcea/downloads/semcor/semcor3.0.tar.gz; then
        echo 'Semcor3.0 could not be automatically downloaded! Please ensure that semcor3.0 is available in this directory as the directory "semcor3.0".'
        echo 'You can download the latest semcor3.0 distribution at http://web.eecs.umich.edu/~mihalcea/downloads.html#semcor'
        exit 2
    elif ! tar -xf semcor3.0.tar.gz; then
        exit 3
    else
        rm -f semcor3.0.tar.gz
    fi
fi

mkdir data_train

echo 'Normalizing semcor XML files and outputting to data_train...'
for filename in ./semcor3.0/brown*/tagfiles/*; do
	cat "$filename" | tidy -xml -iq -o "./data_train/$(basename "$filename").xml" - &> /dev/null
done

mkdir data_key data_test

echo 'Tranforming semcor XML files into sense-annotated key data and plain test data...'
python3 generate_key_test_semcor.py

echo 'Done.'
