import pandas as pd
import nltk
import string
from gensim import corpora, models
from gensim.utils import effective_n_jobs
import collections
import re

# Some Functions from Last Time to get us started:

def negemo_perc(text, liwc_dict):
    '''
    Compute rel. percentage of LIWC 2007 'negemo','death' categories:
    words like "suicide," "desperate," "depress," "cry," 
    '''
    liwc_counts = wordCount(text, liwc_dict)
    
    return (liwc_counts[0]['negemo'] + liwc_counts[0]['death']) / liwc_counts[2]

'''
The following code is adapted from psyLex.
psyLex: an open-source implementation of the Linguistic Inquiry Word Count
Created by Sean C. Rife, Ph.D.
srife1@murraystate.edu // seanrife.com // @seanrife
Licensed under the MIT License
https://github.com/seanrife/psyLex
'''

def readDict(dictionaryPath):
    '''
    Function to read in an LIWC-style dictionary
    '''
    catList = collections.OrderedDict()
    catLocation = []
    wordList = {}
    finalDict = collections.OrderedDict()

    # Check to make sure the dictionary is properly formatted
    with open(dictionaryPath, "r") as dictionaryFile:
        for idx, item in enumerate(dictionaryFile):
            if "%" in item:
                catLocation.append(idx)
        if len(catLocation) > 2:
            # There are apparently more than two category sections; throw error and die
            sys.exit("Invalid dictionary format. Check the number/locations of the category delimiters (%).")

    # Read dictionary as lines
    with open(dictionaryPath, "r") as dictionaryFile:
        lines = dictionaryFile.readlines()

    # Within the category section of the dictionary file, grab the numbers associated with each category
    for line in lines[catLocation[0] + 1:catLocation[1]]:
        catList[re.split(r'\t+', line)[0]] = [re.split(r'\t+', line.rstrip())[1]]

    # Now move on to the words
    for idx, line in enumerate(lines[catLocation[1] + 1:]):
        # Get each line (row), and split it by tabs (\t)
        workingRow = re.split('\t', line.rstrip())
        wordList[workingRow[0]] = list(workingRow[1:])

    # Merge the category list and the word list
    for key, values in wordList.items():
        if not key in finalDict:
            finalDict[key] = []
        for catnum in values:
            workingValue = catList[catnum][0]
            finalDict[key].append(workingValue)
    return (finalDict, catList.values())

def wordCount(data, dictOutput):
    '''
    Function to count and categorize words based on an LIWC dictionary
    '''
    finalDict, catList = dictOutput
    
    # Create a new dictionary for the output
    outList = collections.OrderedDict()

    # Number of non-dictionary words
    nonDict = 0

    # Convert to lowercase
    data = data.lower()

    # Tokenize and create a frequency distribution
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(data)

    fdist = nltk.FreqDist(tokens)
    wc = len(tokens)

    # Using the Porter stemmer for wildcards, create a stemmed version of the data
    porter = nltk.PorterStemmer()
    stems = [porter.stem(word) for word in tokens]
    fdist_stem = nltk.FreqDist(stems)

    # Access categories and populate the output dictionary with keys
    for cat in catList:
        outList[cat[0]] = 0

    # Dictionaries are more useful
    fdist_dict = dict(fdist)
    fdist_stem_dict = dict(fdist_stem)

    # Number of classified words
    classified = 0

    for key in finalDict:
        if "*" in key and key[:-1] in fdist_stem_dict:
            classified = classified + fdist_stem_dict[key[:-1]]
            for cat in finalDict[key]:
                outList[cat] = outList[cat] + fdist_stem_dict[key[:-1]]
        elif key in fdist_dict:
            classified = classified + fdist_dict[key]
            for cat in finalDict[key]:
                outList[cat] = outList[cat] + fdist_dict[key]

    # Calculate the percentage of words classified
    if wc > 0:
        percClassified = (float(classified) / float(wc)) * 100
    else:
        percClassified = 0

    # Return the categories, the words used, the word count, 
    # the number of words classified, and the percentage of words classified.
    return [outList, tokens, wc, classified, percClassified]