import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

def find_word_sense(word, training_data):
    A, B = training_data
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

def process(training_data, test_file):
    output_data = []

    print(' Preprocessing...')
    data = preprocess(open(test_file))

    print(' Determining word senses...')
    for entry in data:
        wf = find_word_sense(entry['word'], training_data)
        output_data.append((entry['word'], wf))

    return output_data