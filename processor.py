import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from features import extract_features

def find_word_sense(entry, training_data):
    A, B = training_data
    word = entry['word']
    if word in B:
        max_sense_prob = 0
        max_sense = None

        word_total_count = B[word][0]
        # Iterate through all senses found for this word
        # Note that none may exist, in which case max_sense will remain None
        for sense, sense_word_count in B[word][1].items():
            sense_total_count = A[sense][0]
            sense_features = A[sense][1]
            
            # Contribute probability that given word will have this sense
            sense_prob = (sense_word_count / word_total_count)
            # Contribute probability that given sense will have this word's lemma
            sense_prob *= (sense_features['lemma'][entry['lemma']] + 1) / (sense_total_count + 1)
            # Contribute probability that given sense will have this word's POS
            sense_prob *= (sense_features['pos'][entry['pos']] + 1) / (sense_total_count + 1)
            # # Contribute probability that given sense will have this word's antecedent
            # sense_prob *= (sense_features['word-1'][entry['word-1']] + 1) / (sense_total_count + 1)
            # Contribute probability that given sense will have this word's antecedent POS
            sense_prob *= (sense_features['pos-1'][entry['pos-1']] + 1) / (sense_total_count + 1)

            if sense_prob > max_sense_prob:
                max_sense_prob = sense_prob
                max_sense = sense

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
    for entry in data:
        wf = find_word_sense(entry, training_data)
        output_data.append((entry['word'], wf))

    return output_data
