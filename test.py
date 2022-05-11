import spacy
import sqlite3
import pandas as pd

def extract_nonstops(text):
    nlp = spacy.load("en_core_web_sm")
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    result = []
    doc = nlp(text.lower())
    for token in doc:
        if not (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            result.append(token.lemma_)
    return result


def extract_all_words(text):
    nlp = spacy.load("en_core_web_sm")
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    result = []
    pos_tag = [ 'ADJ', 'NOUN']
    doc = nlp(text.lower())
    for token in doc:
        if (token.pos_ in pos_tag) and not (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            result.append(token.lemma_)
    return result

def words_count(words):
    kwds = {}
    for w in words:
        if w not in kwds:
            kwds[w]=1
        else:
            kwds[w]+=1
    return kwds

def common_words(words_dict, n=3):
    vals = list(words_dict.values())
    vals.sort(reverse=True)
    words = [k for k,v in words_dict.items() if v >= vals[n-1]]
    return words

def extract_words(text, n=3):
    hotwords = extract_all_words(text)
    words_dict = words_count(hotwords)
    vals = list(words_dict.values())
    vals.sort(reverse=True)
    words = [k for k,v in words_dict.items() if v >= vals[n-1]]
    words = ', '.join(words)
    return words


# Extract default values for 'unitest'

if __name__ == '__main__':

    # Test NLP functions
    text = '''Python is one of the most popular programming languages today
and is easy for beginners to learn because of its readability.
It is a free, open-source programming language with extensive support modules
and community development, easy integration with web services, user-friendly
data structures, and GUI-based desktop applications. '''

    nostops = extract_nonstops(text)
    hotwords = extract_words(text)
    words = extract_all_words(text)
    words_dict = words_count(words)
    keywords = common_words(words_dict)
    print('extract_nonstops >>>', nostops)
    print('extract_all_words >>>', words)
    print('extract_words >>>', hotwords)
    print('words_count  >>>',words_dict)
    print('words_count  >>>',keywords)

    
    
    
    
    
    
    
    
    
import spacy
import keywords as kw
import unittest

text = '''Python is one of the most popular programming languages today 
and is easy for beginners to learn because of its readability.
It is a free, open-source programming language with extensive support modules 
and community development, easy integration with web services, user-friendly 
data structures, and GUI-based desktop applications. '''

# String to perform the assessment in the 'extract_words' test   
s = 'programming, language, easy'

# Dictionary to perform the assessment in the 'test_count' test   
d = {'popular': 1, 'programming': 2, 'language': 2, 'today': 1, 'easy': 2, 'beginner': 1, 'readability': 1, 'free': 1, 'open': 1, 'source': 1, 'extensive': 1, 'support': 1, 'module': 1, 'community': 1, 'development': 1, 'integration': 1, 'web': 1, 'service': 1, 'user': 1, 'friendly': 1, 'datum': 1, 'structure': 1, 'gui': 1, 'desktop': 1, 'application': 1}


class TestStringMethods(unittest.TestCase):
    
 
    def test_hotwords(self):
        # This function tests the 'kw.extract_words(text)' function
        # Do not modify the function name
        # Insert your code here:

    def test_count(self):
        # This function tests the 'kw.words_count' function
        # Requires to use 'kw.extract_all_words(text)' as an intermediate step to get the words list        
        # Do not modify the function name
        # Insert your code here:

if __name__ == '__main__':
    unittest.main()
