The closest_words function can be used to work out what dictionary words are closest to your name (in the spell-checker sense of closest).

For example:

$ python3 -m venv venv
$ source venv/bin/activate
$ pip install nltk
$ python
>>> import nltk
>>> word_tag_pairs = nltk.corpus.brown.tagged_words()
>>> no_proper_nouns = [p for p in word_tag_pairs if not p[1].startswith('NP')]
>>> words = [p[0] for p in no_proper_nouns]
>>> words = [w.lower() for w in words]
>>> import re
>>> words = [w for w in words if re.match(r'^[a-z]\D*$', w)]
>>> words = list(set(words))
>>> words.sort()
>>> import levenshtein
>>> levenshtein.closest_words(words, 'thomas')
>>> levenshtein.closest_words(words, 'smith')

