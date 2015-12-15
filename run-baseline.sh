#!/bin/bash

if [ ! -d 'data_test' ]; then
    echo 'Test data not found! Normalizing semcor...'
    if ! ./normalize_semcor.sh; then
        exit 2
    fi
fi

echo "Evaluating with file $1..."
python3 baseline.py data_train "data_test/$1.txt" "output/$1.baseline_txt" &&

echo 'Scoring...' &&
python3 output/score.py "data_key/$1.txt" "output/$1.baseline_txt" > "output/$1.baseline_score"
