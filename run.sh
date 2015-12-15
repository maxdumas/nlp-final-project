#!/bin/bash

if [ ! -d 'data_test' ]; then
    echo 'Test data not found! Normalizing semcor...'
    if ! ./normalize_semcor.sh; then
        exit 2
    fi
fi

if [ ! -d 'output' ]; then
    mkdir output
fi

echo "Evaluating with file $1..."
python3 nbc.py data_train "data_test/$1.txt" "output/$1.txt" &&

echo 'Scoring...' &&
python3 score.py "data_key/$1.txt" "output/$1.txt" > "output/$1.score"
