# this file gets keywords from url and finds relevant tweets based on input -- does kcluster to grab more relevant tweets

import requests
import newspaper
import nltk
import rake
import html2text
import operator
import tweepy
import json
import re
from nltk.tokenize import word_tokenize
from newspaper import Article
from tweepy.streaming import StreamListener
from nltk.corpus import stopwords
import string
from test import TweetsClustering
 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

class MyStreamListener(StreamListener):
    
    def __init__(self):
        self.list_of_tweets = []

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            with open('tweets.json', 'a') as f:
                f.write(data)
                f.write(",")
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)

def mains():
    '''CONSUMER_KEY = "5k315aJtfEpZOftsOpOIPrvai"
    CONSUMER_SERCRET = "wicLMZQQGnQi7oqMYCZVJyRNilz29PMZQSHDetKM4i8fIUfkZv"
    ACCESS_TOKEN = "65937816-xVJP9P4oVbBbJkVs1Sarq7N2sqRI8WKGY9HG5Igzm"
    ACCESS_TOKEN_SECRET = "HlorBQc8xaKXq1KdUirQx90eIBLofkilBNvbUOid83K9R"

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SERCRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    '''
    url = raw_input("enter URL:")
    dataset = raw_input("enter dataset:")
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    html = article.html
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text = text_maker.handle(html)
    #print(article.summary)
    #print(article.authors)
    print(article.title)
    #title_split = (article.title).split(" ")
    #keywords = title_split[:]
    keywords = article.keywords
    #print(text)


    rake_object_title = rake.Rake("SmartStoplist.txt")
    rake_object_html = rake.Rake("SmartStoplist.txt", 5, 3, 2) #5 3 2
    rake_object_summary = rake.Rake("SmartStoplist.txt", 5, 3, 2)
    keywords_html = rake_object_html.run(text)
    title_keys = rake_object_title.run(article.title)
    #print("Keywords on html:", keywords_html)
    keywords_summary = rake_object_summary.run(article.summary)
    count = 0
    for i in range(len(keywords_html)):
        keywords.append(keywords_html[i][0])
        count = count + 1
        if count > 4:
            break
    for i in range(len(title_keys)):
        keywords.append(title_keys[i][0])
    
    for i in range(len(keywords_summary)):
        keywords.append(keywords_summary[i][0])

    for i in range(len(keywords)):
        keywords[i] = keywords[i].encode("utf-8")

    #print keywords


    t = TweetsClustering(50, dataset)
    t.preprocessTweet()
    #t.getJaccard()
    #t.determineCentroids()
    #t.initializeClusters()
    #t.convergeClusters()

    list_of_ids = []
    for i in t.parsedTweets:
        count = 0;
        #if any(texzt in i['text'] for keyword in keywords):
        for key in keywords:
            if(key in i['text']):
                count = count + 1
                #print(i['text'])
                #list_of_ids.append(i['id'])        
        if count >= 4:
            #print(i['text'])
            list_of_ids.append(i['id'])
    #print (list_of_ids)

    print (len(list_of_ids))
    t.setClusterNum(len(list_of_ids))   
    t.getJaccard()
    t.determineCentroids()
    t.initializeClusters()
    t.convergeClusters()

    list_of_centroids = []
    for i in list_of_ids:
        found = False
        for c in t.centroids:
            if found == True:
                break
            if i == c:
                list_of_centroids.append(c)
                found = True
                break
            else:   
                for ci in t.clusters[c]:
                    if i == ci:
                        list_of_centroids.append(c)
                        found = True
                        break #ideally breaks out of else
    print(list_of_centroids)
    list_of_tweets = []
    list_of_centroid = set(list_of_centroids)
    print(list_of_centroid)
    print (len(list_of_centroid))
    #list_of_tweets = []
    for c in list_of_centroid:      
        for ci in t.clusters[c]:
            #print(ci)
            list_of_tweets.append(t.parsedTweets[ci]['entiretext'])

    #print(list_of_tweets)
    print(len(list_of_tweets))
    return list_of_tweets
    
