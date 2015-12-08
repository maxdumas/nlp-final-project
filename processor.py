import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

def find_word_sense(entry, training_data):
    A, B = training_data
    word = entry['word']
    if word in B:
        max_sense_prob = 0
        max_sense = None

        word_total_count = B[word][0]
        # Iterate through all senses found for this word:
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

    for i in range(1, len(lemma_tagged)):
        lemma_tagged[i]['word-1'] = lemma_tagged[i - 1]['word']
        lemma_tagged[i]['pos-1'] = lemma_tagged[i - 1]['pos']
    lemma_tagged[0]['word-1'] = '.'
    lemma_tagged[0]['pos-1'] = '.'

    return lemma_tagged

def process(training_data, test_file):
    output_data = []

    print(' Preprocessing...')
    data = preprocess(open(test_file))

    print(' Determining word senses...')
    for entry in data:
        wf = find_word_sense(entry, training_data)
        output_data.append((entry['word'], wf))

    return output_data