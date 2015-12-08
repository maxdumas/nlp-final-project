import xml.etree.ElementTree as ET
import os

def generate_key(word_form):
    if 'lexsn' in word_form.attrib and 'lemma' in word_form.attrib:
        lemma = word_form.attrib['lemma']
        lexsn = word_form.attrib['lexsn']
        return '{}%{}'.format(lemma, lexsn)
    else:
        return ''

for filename in os.listdir('training_data'):
    with open(os.path.join('key_data', os.path.splitext(filename)[0] + '.txt'), 'w') as key_file:
        with open(os.path.join('test_data', os.path.splitext(filename)[0] + '.txt'), 'w') as test_file:
            tree = ET.parse(os.path.join('training_data', filename))
            root = tree.getroot()
            file = root[0]
            for paragraph in file:
                for sentence in paragraph:
                    for word_form in sentence:
                        print('{} {}'.format(word_form.text, generate_key(word_form)).strip(), file=key_file)
                        print(word_form.text.strip(), file=test_file)
