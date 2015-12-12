def extract_features(word_form, i, sentence):
    n = len(sentence)
    features = {}

    features['word'] = word_form['word']
    features['pos'] = word_form['pos']
    features['lemma'] = word_form['lemma']

    # Extract collocation features from k previous and k following forms
    for k in range(-5, 5):
        if k == 0: continue

        if i + k < -1 or i + k >= n:
            features['pos{:+}'.format(k)] = None
        elif i + k == -1:
            features['pos{:+}'.format(k)] = '.'
        elif 'pos' in sentence[i + k]:
            features['pos{:+}'.format(k)] = sentence[i + k]['pos']

    return features
