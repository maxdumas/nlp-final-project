# Word Sense Disambiguation

- The task of determining which sense of a word is in use at a given location in an input text
- Chosen inventory of sense should vary significantly based on the task; overgeneralization will lead to worse performance
- Lexical sample tasks:
	- Small subset of corpus words is chosen, each with an inventory of word senses from a lexicon
	- Words are hand-labeled with the correct sense
	- Machine learning techniques are leveraged to train upon these lexical samples
- All words tasks:
	- Very similar to POS tagging, but with a much larger problem set
	- Entire text and lexicon is provided, system must disambiguate all terms
	- Often less practical due to a lack of training data for all word senses

## Supervised Word Sense Disambiguation

- For supervised machine learning in the lexical sample task, there are a number of corpora available for assisting in system training (See 20.2)

### Extracting Feature Sets for Supervised Learning

- What minimum amount of context allows us to determine the sense of a word unambiguously?
- Sentence is typically preprocessed to include information like part-of-speech, lemma forms, and sometimes more advanced syntactic parsing like dependency relations
- Features illuminating the context of each given word are then extracted for each word. These features are typically stored in vectors (Why?)
	- Collocation features provide information about words located in specific positions relative to the target word, and usually include the word itself, its root form, and its POS
	- Bag-of-words features typically contain a set of binary flags indicating the presence of a specific set of words relevant to the target word within a fixed window to it.

### Naive Bayes and Decision List Classifiers

- Really any supervised machine learning paradigm can be used to 
- Naive Bayes Classifier
	- For any given word, choose the sense which is most probably given the feature vector
	- To limit the probabilistic space to one which can be well-covered by our training data, we assume (naively) that each feature in the feature set is independent of all the others.
	- This allows us to estimate the probability of the feature set given a certain sense as the product of the probabilities of each individual feature given that sense.
	- Thus our formulation then becomes: choose the sense that maximizes the product of its own probability P(s) of occuring and the product of the probabilities of all features P(f_j|s) occurring given that sense.
- Training Bayes
	- For each sense s_i, we calculate P(s_i) as the number of times the target word occurs in that sense over the number of times the target word occurs
	- For each feature f_j, we calculate P(f_j|s_i) as the number of times that feature occurs for that sense over the number of times that sense occurs
