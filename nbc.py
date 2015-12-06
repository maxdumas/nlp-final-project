import argparse
from collections import defaultdict
import xml.etree.ElementTree as ET
import os
import re
import sys

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import nltk

def cl(i, minv, maxv):
    return sorted((minv, maxv - 1, i))[1]

def generate_key(word_form):
    lemma = word_form.attrib['lemma']
    lexsn = word_form.attrib['lexsn']
    return '{}%{}'.format(lemma, lexsn)

def parse_xml(filenames, operation):
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        file = root[0]
        for paragraph in file:
            for sentence in paragraph:
                for i in range(len(sentence)):
                    word_form = sentence[i]
                    # Choose only tagged words
                    if 'cmd' in word_form.attrib \
                    and 'lemma' in word_form.attrib \
                    and word_form.attrib['cmd'] == 'done' \
                    and 'ot' not in word_form.attrib:
                        operation(word_form, i, sentence)

def extract_features(word_form, i, sentence):
    n = len(sentence)
    features = {}

    features['pos'] = word_form.attrib['pos']
    features['lemma'] = word_form.attrib['lemma']

    prev_form = sentence[cl(i - 1, 0, n)]

    if 'pos' in prev_form.attrib:
        features['prev_pos'] = prev_form.attrib['pos']
    features['prev_word'] = prev_form.text

    return features

def calcA(filenames):
    output = defaultdict(lambda: [0, defaultdict(lambda: defaultdict(int))])

    def operate(word_form, i, sentence):
        feature_set = extract_features(word_form, i, sentence)
        key = generate_key(word_form)
        # Increment total count for sense
        output[key][0] += 1
        # For each found feature, increment
        # count for that feature-value pair
        for feature, value in feature_set.items():
            kvp = '{}-{}'.format(feature, value)
            output[key][1][feature][value] += 1

    parse_xml(filenames, operate)

    return output

def calcB(filenames):
    output = defaultdict(lambda: [0, defaultdict(int)])

    def operate(word_form, i, sentence):
        word = word_form.text
        key = generate_key(word_form)
        # Increment total count for word
        output[word][0] += 1
        # Increment count for word in this sense
        output[word][1][key] += 1

    parse_xml(filenames, operate)

    return output

def train(training_dir):
    filenames = {os.path.join(training_dir, filename) for filename in os.listdir(training_dir)}

    # We want to calculate the following:
    # A: Total count of each sense
    # A: Count of each feature per sense
    # B: Count of each sense per word
    # B: Total count of each word

    print(' Calculating feature-sense concordances...')
    # A := { s_i: [c_i { f_j:v(f_j): c_f_j}]}
    A = calcA(filenames)

    print(' Calculating word-sense counts...')
    # B := { w_i: [c_i, { s_w_i: c_w_i }]}
    B = calcB(filenames)

    return (A, B)

def find_word_sense(word, B):
    # Use the lemma form that has the synset with the highest count
    max_count = 0
    max_sense_key = None
    # for lemma in possible_lemmas:
    if word in B:
        for sense_key, count in B[word][1].items():
            if max_count < count:
                max_sense_key = sense_key
                max_count = count

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

def process(sense_counts, test_file):
    output_data = []

    print(' Preprocessing...')
    data = preprocess(open(test_file))

    print(' Determining word senses...')
    for entry in data:
        wf = find_word_sense(entry['word'], sense_counts)
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
