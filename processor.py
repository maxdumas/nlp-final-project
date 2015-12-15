import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from features import extract_features

def find_word_sense(entry, training_data, f):
    A, B = training_data
    word = entry['word']
    if word in B:
        max_sense_prob = 0
        max_sense = None
        word_total_count = B[word][0]
        print(dict(entry), file=f)
        print('Total Word Occurrences: {}'.format(word_total_count), file=f)
        print('Senses: {}'.format(dict(B[word][1])), file=f)
        # Iterate through all senses found for this word
        # Note that none may exist, in which case max_sense will remain None
        for sense, sense_word_count in B[word][1].items():
            sense_total_count = A[sense][0]
            sense_features = A[sense][1]
            print('Sense {}'.format(sense), file=f)
            print('  Total Sense Occurrences: {}'.format(sense_total_count), file=f)
            print('  Total Sense Occurrences with word {}: {}'.format(word, sense_word_count), file=f)
            print('  Features: {}'.format(dict(sense_features)), file=f)
            # Contribute probability that given word will have this sense
            sense_prob = (sense_word_count) / (word_total_count)
            print('  P(s|w): {}'.format(sense_prob), file=f)
            # Contribute all feature-sense probabilities with Laplace Smoothing
            for feature in sense_features:
                if feature != 'word':
                    contrib = 0
                    if feature.split(':')[0] == 'q':
                        contrib = (sense_features[feature][entry[feature]]) / (sense_total_count)
                    else:
                        contrib = (sense_features[feature][entry[feature]] + 10) / (sense_total_count + 10)

                    print('    Feature {} = {}'.format(feature, entry[feature]), file=f)
                    sense_prob *= contrib
                    print('    P(f|s): {}'.format(contrib), file=f)
                    print('    P(s) is now {}'.format(sense_prob), file=f)

            if sense_prob > max_sense_prob:
                print('Sense {} is now the most probable sense for word {} at {}'.format(sense, word, sense_prob), file=f)
                print('Previous maximum was {} at {}'.format(max_sense, max_sense_prob), file=f)
                max_sense_prob = sense_prob
                max_sense = sense
        print('----------', file=f)

        return max_sense

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
    tokens = [line.strip() for line in file]

    # Generate all word POS tags
    print('  Tagging parts of speech...')
    pos_tagged = nltk.pos_tag(tokens)

    # Generate all word lemma forms
    print('  Finding lemma forms...')
    l = lemmatizer()
    lemma_tagged = [{'word': token, 'lemma': l(token, pos), 'pos': pos} for (token, pos) in pos_tagged]

    # Make a list of lists
    # Go through all words, appending to a list within the list
    # If the word POS is '.', then flush the current list to the sentence list with that word
    # Then start working with a new list
    sentence_chunked = []
    current_sentence = []
    for word_form in lemma_tagged:
        current_sentence.append(word_form)

        if word_form['pos'] == '.':
            sentence_chunked.append(current_sentence)
            current_sentence = []

    feature_tagged = []
    for sentence in sentence_chunked:
        for i in range(0, len(sentence)):
            word_form = sentence[i]
            feature_tagged.append(extract_features(word_form, i, sentence))

    return feature_tagged

def process(training_data, test_file):
    output_data = []

    print(' Preprocessing...')
    data = preprocess(open(test_file))

    print(' Determining word senses...')
    with open('output.log', 'w') as f:
        for entry in data:
            wf = find_word_sense(entry, training_data, f)
            output_data.append((entry['word'], wf))

    return output_data
