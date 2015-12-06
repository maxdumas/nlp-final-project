import argparse
from collections import defaultdict
import xml.etree.ElementTree as ET
import os
import re

from nltk.corpus import wordnet as wn

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
                    sense_counts[lemma][key]['count'] += 1

                    # Key by lemma
                    # Store all found sense_keys for that lemma along with counts for each

def find_word_sense(word, sense_counts):
    # Use WordNet to look up lemmas for given words:
    # {lemma.name() for ss in wn.synsets('cared') for lemma in ss.lemmas()}
    possible_lemmas = {lemma.name() for ss in wn.synsets(word) for lemma in ss.lemmas()}
    
    # Use the lemma form that has the synset with the highest count
    max_count = 0
    max_sense_key = None
    for lemma in possible_lemmas:
        if lemma in sense_counts:
            for sense_key, v in sense_counts[lemma].items():
                if max_count < v['count']:
                    max_sense_key = sense_key
                    max_count = v['count']

    # if max_sense_key == None:
    #     print('Chosen form {} for {} after looking at {}'.format(max_sense_key, word, possible_lemmas))

    return max_sense_key

def main(training_dir, test_file, output_file):
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

    # for fuck in sense_counts:
    #     print(fuck)
    #     for shit, piss in sense_counts[fuck].items():
    #         print('  {} = {}'.format(shit, piss))
    
    # When all training files have been looked at,
    # operate on test file, choosing for each word the sense
    # that is used the most times in the training data

    # If the given word does not exist, assume it is a
    # closed-class word and ignore it.
    with open(test_file) as test_file:
        with open(output_file, 'w') as output_file:
            for line in test_file:
                word = line.strip()
                if len(word) != 0:
                    wf = find_word_sense(word, sense_counts)
                    print('{} {}'.format(word, wf or ''), file=output_file)

    print('Done.')

parser = argparse.ArgumentParser()
parser.add_argument('training_dir')
parser.add_argument('test_file')
parser.add_argument('output_file')
args = parser.parse_args()

main(args.training_dir, args.test_file, args.output_file)
