from collections import defaultdict
import os
import xml.etree.ElementTree as ET

from features import extract_features

def cl(i, minv, maxv):
    return sorted((minv, maxv - 1, i))[1]

def generate_key(word_form):
    lemma = word_form['lemma']
    lexsn = word_form['lexsn']
    return '{}%{}'.format(lemma, lexsn)

def parse_xml(filenames, operation):
    for filename in filenames:
        tree = ET.parse(filename)
        root = tree.getroot()
        file = root[0]
        for paragraph in file:
            for sentence in paragraph:
                simplified_sentence = [];
                for word_form in sentence:
                    # Choose only tagged words
                    if 'cmd' in word_form.attrib \
                    and 'lemma' in word_form.attrib \
                    and word_form.attrib['cmd'] == 'done' \
                    and 'ot' not in word_form.attrib:
                        simplified_word_form = defaultdict(lambda: None)
                        simplified_word_form.update(word_form.attrib)
                        simplified_word_form['word'] = word_form.text

                        simplified_sentence.append(simplified_word_form)
                
                for i in range(0, len(simplified_sentence)):
                    word_form = simplified_sentence[i]
                    operation(word_form, i, simplified_sentence)

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
            output[key][1][feature][value] += 1

    parse_xml(filenames, operate)

    return output

def calcB(filenames):
    output = defaultdict(lambda: [0, defaultdict(int)])

    def operate(word_form, i, sentence):
        word = word_form['word']
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
    # A := { s_i: [c_i { f_j: { v(f_j): c_f_j }}]}
    # That is:
    #   A[sense][0] is the total count of all occurrences of that sense
    #   A[sense][1] is a dictionary of all features applied to that sense
    #   A[sense][1][feature] is a dictionary of all values found for that feature-sense
    #   A[sense][1][feature][value] is the count of the number of times that value-feature-sense was found
    A = calcA(filenames)

    print(' Calculating word-sense counts...')
    # B := { w_i: [c_i, { s_w_i: c_w_i }]}
    # That is:
    #   B[word][0] is the total count of all occurrences of that word
    #   B[word][1] is a dictionary of all senses that were found for that word
    #   B[word][1][sense] is the count of the number of times that sense-word was found
    B = calcB(filenames)

    return (A, B)
