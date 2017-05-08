# HeadlineSentimentAnalysis
Framework for Headline Sentiment Analysis

Whitney Choo, So Yon Kwon

To anaylze sentiment of current headlines: 

python analyzesentiment_current.py

input: url of headline
output: sentiment


Needed libraries:

libsvm
newspaper
nltk
html2text
tweepy
rake
requests




Other files:

data: directory containing all data 

sentimentmodified.py: SVM model for analyzing sentiment of tweet datasets with appended sentiments

sentimentmodifiedcurrent.py: SVM model for analyzing sentiment of current tweets

merging: merge SVM model with keyword extractor of pre-existing tweet datasets

merging_current.py: merge SVM model with current tweet extractor

randomize.py: randomize training set

test.py: k-clustering algorithm and necessary preprocessing components

analyzesentiment.py: obtains keywords and tweets from dataset to be supplied to SVM



GITHUB LINK:
https://github.com/kwon212/HeadlineSentimentAnalysis


