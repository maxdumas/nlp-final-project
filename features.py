from collections import defaultdict
from nltk.corpus import wordnet as wn

def extract_features(word_form, i, sentence):
    n = len(sentence)
    features = defaultdict(lambda: None)

    features['word'] = word_form['word']
    features['q:pos'] = word_form['pos'][:2]
    features['q:lemma'] = word_form['lemma']

    # Extract collocation features from k previous and k following forms
    for k in range(-1, 2):
        if k == 0: continue

        if i + k < -1 or i + k >= n:
            features['c:pos{:+}'.format(k)] = None
        elif i + k == -1:
            features['c:pos{:+}'.format(k)] = '.'
        else:
            features['c:pos{:+}'.format(k)] = sentence[i + k]['pos'][:2]

    # Extract bag-of-words features from k previous and k following forms
    for k in range(-2, 0):
        if k == 0: continue

        features['b:near_sentence_start'] = i + k <= -1
    return features
