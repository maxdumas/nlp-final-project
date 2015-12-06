#!/bin/bash
mkdir ./training_data

for filename in ./semcor3.0/brown1/tagfiles/*; do
	cat "$filename" | tidy -xml -i - > "./training_data/$(basename "$filename").xml"
done

for filename in ./semcor3.0/brown2/tagfiles/*; do
        cat "$filename" | tidy -xml -i - > "./training_data/$(basename "$filename").xml"
done

for filename in ./semcor3.0/brownv/tagfiles/*; do
        cat "$filename" | tidy -xml -i - > "./training_data/$(basename "$filename").xml"
done
