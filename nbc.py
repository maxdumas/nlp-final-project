import argparse
from collections import defaultdict
import xml.etree.ElementTree as ET
import os
import re
import sys

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import nltk

def generate_key(word_form):
    lemma = word_form.attrib['lemma']
    lexsn = word_form.attrib['lexsn']
    return '{}%{}'.format(lemma, lexsn)

def parse_xml(tree, sense_counts):
    root = tree.getroot()
    file = root[0]
    for paragraph in file:
        for sentence in paragraph:
            for word_form in sentence:
                # Choose only tagged words
                if 'cmd' in word_form.attrib \
                and 'lemma' in word_form.attrib \
                and word_form.attrib['cmd'] == 'done' \
                and 'ot' not in word_form.attrib:
                    # Construct fully-qualified WordNet lemma name using wf attributes
                    key = generate_key(word_form)
                    lemma = word_form.attrib['lemma']
                    # Add to dictionary, incrementing count
                    # Key by lemma
                    # Store all found sense_keys for that lemma along with counts for each
                    sense_counts[lemma][key]['count'] += 1

def train(training_dir):
    # Create dictionaries for storing word frequencies
    sense_counts = defaultdict(
        lambda: defaultdict(
            lambda: { 'count': 0 }))

    # Load training file(s)
    filenames = os.listdir(training_dir)
    for filename in filenames:
        # Parse File with XML Parser
        tree = ET.parse(os.path.join(training_dir, filename))
        parse_xml(tree, sense_counts)

    return sense_counts

def find_word_sense(lemma, sense_counts):
    # Use the lemma form that has the synset with the highest count
    max_count = 0
    max_sense_key = None
    # for lemma in possible_lemmas:
    if lemma in sense_counts:
        for sense_key, v in sense_counts[lemma].items():
            if max_count < v['count']:
                max_sense_key = sense_key
                max_count = v['count']

    # if max_sense_key == None:
    #     print('Chosen form {} for {} after looking at {}'.format(max_sense_key, word, possible_lemmas))

    return max_sense_key

def lemmatizer():
    lmtzr = WordNetLemmatizer()

    def r(token, pos):
        if pos[0] == 'N':
            return lmtzr.lemmatize(token, wn.NOUN)
        elif pos[0] == 'V':
            return lmtzr.lemmatize(token, wn.VERB)
        elif pos[0] == 'J':
            return lmtzr.lemmatize(token, wn.ADJ)
        elif pos[0] == 'R':
            return lmtzr.lemmatize(token, wn.ADV)
        else:
            return None

    return r

def preprocess(file):
    print('  Tokenizing...')
    tokens = nltk.word_tokenize(file.read())

    # Generate all word POS tags
    print('  Tagging parts of speech...')
    pos_tagged = nltk.pos_tag(tokens)

    # Generate all word lemma forms
    print('  Finding lemma forms...')
    l = lemmatizer()
    lemma_tagged = [{'word': token, 'lemma': l(token, pos), 'pos': pos} for (token, pos) in pos_tagged]

    return lemma_tagged

def extract_features(data):
    
    return data

def process(sense_counts, test_file):
    output_data = []

    print(' Preprocessing...')
    data = preprocess(open(test_file))

    print(' Extracting features...')
    data = extract_features(data)

    print(' Determining word senses...')
    for entry in data:
        wf = find_word_sense(entry['lemma'], sense_counts)
        output_data.append((entry['word'], wf))

    return output_data


def output_result(final_data, output_file):
    with open(output_file, 'w') as file:
        for (word, wf) in final_data:
            print('{} {}'.format(word, wf or '').strip(), file=file)

def main(training_dir, test_file, output_file):
    print('Training...')
    training_data = train(training_dir)

    print('Processing...')
    final_data = process(training_data, test_file)
    
    print('Writing results...')
    output_result(final_data, output_file)

    print('Done.')

parser = argparse.ArgumentParser()
parser.add_argument('training_dir')
parser.add_argument('test_file')
parser.add_argument('output_file')
args = parser.parse_args()

main(args.training_dir, args.test_file, args.output_file)
