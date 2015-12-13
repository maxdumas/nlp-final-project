#!/bin/bash
mkdir data_train

echo 'Normalizing semcor XML files and outputting to data_train...'
for filename in ./semcor3.0/brown*/tagfiles/*; do
	cat "$filename" | tidy -xml -iq -o "./data_train/$(basename "$filename").xml" - &> /dev/null
done

mkdir data_key data_test

echo 'Tranforming semcor XML files into sense-annotated key data and plain test data...'
python3 generate_key_test_semcor.py

echo 'Done.'

# for filename in ./semcor3.0/brown2/tagfiles/*; do
#     cat "$filename" | tidy -xml -i - > "./training_data/$(basename "$filename").xml"
# done

# for filename in ./semcor3.0/brownv/tagfiles/*; do
#     cat "$filename" | tidy -xml -i - > "./training_data/$(basename "$filename").xml"
# done
