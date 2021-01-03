#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Determine the "Crispness Index" (CI) for an input file.

Defined by D. David Bourland as:

  C.I. = Number of E-Prime Sentences / Total Number of Sentences

E-Prime is the subset of english that does not include the verb "to be"
or any of its conjugations or forms.
"""

import nltk.data # type: ignore
import string
import sys

not_eprime = ["be", "being", "been", "am", "is", "isn't", "are", "aren't",
              "was", "wasn't", "were", "weren't", "i'm", "you're", "we're",
              "they're", "he's", "she's", "it's", "there's", "here's",
              "where's", "how's", "what's", "who's", "that's", "ain't"]

## Translation tables
# replace whitespace (space, newline, CR, etc.) with space characters
whitespace_table = str.maketrans(string.whitespace, ' '*6)
# replace normal punctuation (except apostrophes) with spaces
punct_table = str.maketrans(".,\"", " "*3)

def is_eprime(sent: str) -> bool:
    """Determine if a sentence is e-prime."""
    # Replace punctuation with whitepace
    words_punct = sent.translate(punct_table)
    # break sentence into words
    words = words_punct.split(" ")
    # Replace any right directional quotes with ascii quotes
    words_norm = [ x.replace("’", "'") for x in words]
    # TODO: Replace any punctuation at the beginning or end of words
    # lowercase words
    words_lower = [x.lower() for x in words_norm]
    intersection = [word for word in words if word in not_eprime] 
    if len(intersection) == 0:
        return True
    else:
        return False

# Convert all whitespace to simple spaces
def remove_newlines(sentence: str) -> str:
    return sentence.translate(whitespace_table)

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
fp = open(sys.argv[1])
data = fp.read()
eprime_count = 0
total_count = 0
print("== The following sentences were not E-Prime ==\n")
for sent in tokenizer.tokenize(data):
    total_count += 1
    #sentence_words = word_tokenize(sent)
#    sentence_words_nopunct = [x.translate(nopunct_table) for x in sentence_words]
    oneline = remove_newlines(sent)
    if is_eprime(oneline):
        eprime_count += 1
    else:
        print(oneline)
        print()
if total_count > 0:
    print("Analyzed {} sentences, {} were E-Prime ({:.2f}%)"
        .format(total_count, eprime_count, 100*eprime_count/total_count))
