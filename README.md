# Natural Language Processing Fall 2015 Final Project:

## Sense Disambiguation with the Naive Bayes Classifier

### Maximillian Dumas

## Installation

This project requires Python 3 and pip3. It also requires NLTK. You can install NLTK using pip by executing:

```
pip install nltk
```

## Running

To run this project, simply execute `./run-all.sh` from a terminal window. This will run the NBC on all available input files. All output will be directed to `./output`.

If you would like to run the NBC on a specific file, execute `./run.sh file_name` where file_name is the name of an XML file in the `./data_train` folder (without an extension). For example, to run the NBC against file `./data_train/br-a01.xml`, run the command `./run.sh br-a01`.
