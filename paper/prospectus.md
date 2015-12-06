# Problem Statement

An incredibly important aspect of computational understanding of human language is word meaning. Without word meaning, it is effectively impossible to determine the meaning of sentences and thus entire examined text. The meaning of a word most concisely is its definition and part of speech; its *sense*, though other factors, namely categorical information like its hypernyms, provide useful information as well. The information provided to us by word meaning can affect the classification of a text, the answer to a question, the summary generated from a text, and the information extracted from a text. Thus being able to effectively determine the meaning of words in a given text is essential, but it is often impractical to do so by hand. Humans are exceptionally good at determining the senses of words in context, and our language is built around that. However, this makes the task of word sense disambiguation exceptionally difficult for computers, as our language is full of homonyms and homographs, and many words are often used with different senses in extremely subtle ways. Yet computers must be able to parse and understand our words if we are to empower them with our language, and we cannot annotate all texts manually. Thus enters the field of word sense disambiguation, which aims to provide computers with the tools to automatically determine the sense of words in a given context. The desired end result of a word sense disambiguation task is that all words in the input have been assigned a single, correct sense that correctly reflects the text's real meaning.

# Description

We will be implementing a Naive Bayes Classifier for this project as the algorithm for word sense disambiguation.

## Baseline

The baseline algorithm we will use to determine the performance of our classifier will be to, for each target word, choose the sense of that word that occurs the most frequently in the training data.

## Pre-processing

In order to be able to accurately and effectively determine the senses of words in a text, it is essential to provide as much rich contextual information about each word as possible. To this effect, input text will be pre-processed to determine various pieces of information like parts-of-speech, lemma forms, and if feasible, more advanced information like dependency relations. To this effect we will use available third-party tools wherever possible, as the determination of these data is not the focus of this project. The text will be processed into a structured data format augmented with this processed information.

## Feature Extraction

Once all preliminary information has been computed and is available, feature extraction will begin to corrolate information that will be useful in training the Naive Bayes classifier. The focus of these features will be to illuminate the context of the target word, and will be broken into two categories: collocation features and bag-of-words features.

Collocation features will provide information about words in specific positions relative to the target word, such as its direct neighbors or secondary neighbors. Features extracted may include but are not limited to the neighbor's part-of-speech and the word itself.

Bag-of-words features will provide information about the binary presence of information within a fixed window of the target word. This may include indicating the presence of specific words that are relevant to a given sense of the word, parts-of-speech that may indicate a relevant sense of the word is in use, or other phenomena.

The exact set of features chosen will be a significant part of the challenge of this project, and have significant effect on its results.

These features will be stored in sets as part of the augmented data structure constructed during pre-processing.

## Training

Training involves the calculation of required probabilities for computing the Naive Bayes classifier formula. The first set of those probabilities is each of P(s_i), which is the probability of a given word sense s_i. We will calculate this as the number of times the target word occurs as sense s_i in our training corpus, divided by the number of times the target word ocurs in the training corpus total.

The second set is each of P(f_j|s_i), which is the probability that each feature occurs for a given word sense s_i. We calculate this as the number of times that feature occurs for that sense in the training corpus, divide by the number of times that sense occurs in the training corpus.

With these values computed, we will be prepared to compute the senses for each word in the corpus. For words that we encounter that were not present in the training data, it will be necessary to find a suitable default resolution strategy.

## The Algorithm

For each target word in the input text, we will assign it the the sense s which maximizes the product of the probability of its own occurrence P(s) and the product of the probabilities of all features P(f_j|s) ocurring given that sense. That is:

<formula here>

## Evaluation

We will evaluate our computed word senses against a test corpus for which we will have known word senses already available. From this we will compute our algorithmic accuracy. We will compare this accuracy against the baseline system, which will be run against the same test data. The corpus that we will use as our test data is to be determined. Jurasky and Martin notes that the reasonable ceiling for this task in at most 90%, though expectedly around 75%, which is what most human inter-annotator agreement tops out at.