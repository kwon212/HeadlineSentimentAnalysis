import requests
import newspaper
import nltk
import rake
import html2text
import operator
import tweepy
import json
import re
from collections import Counter
from nltk.tokenize import word_tokenize
from newspaper import Article
from tweepy.streaming import StreamListener
from nltk.corpus import stopwords
import string
import sentimentmodifiedcurrent as sentiment


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']
stop.append("Advertisement")
stop.append("Continue")
stop.append("with")
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
    def __init__(self, api = None):
        super(MyStreamListener, self).__init__()
        self.counter = 0
        self.limit = 1000
        self.tweetList = []
            
    def on_status(self, status):
        if self.counter < self.limit:
            #print(self.counter) 
            self.counter = self.counter + 1
            try:
                with open('tweets.txt', 'a') as f:
                    #f.write(str(self.counter))
                    f.write((status.text).encode("utf-8"))
                    f.write("\n")
                    f.write("##########")
                    f.write("\n")
                f.close()
            except (TypeError, NameError):
                print(TypeError + " " + NameError)  
        else: 
            myStream.disconnect()
    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    url = raw_input("Please enter your url for your news article: ")
    #url = "https://www.nytimes.com/2017/03/21/climate/trump-climate-change.html"
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    html = article.html
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    print ("Title: "+article.title.encode("utf-8"))
    print ("Your sentiments are being generated...")
    l = list(article.title.encode("utf-8").split())
    text = text_maker.handle(html)
    l = [li for li in l if li.lower() not in stop]
    #c=Counter(l)
    #c = c.most_common(2)
    #print c
    #print(article.title)
    #k#eywords = l 
    f = open("headlinesentiment.txt","r")
    c = 0
    maxjc = 2
    healinel = -1
    ps = f.readlines()
    ps = [x.strip() for x in ps]
    for line in ps:
        if c % 3 == 0:
           
           
             s1 = set(line.split())
             #print s1
             s2 = set(article.title.encode("utf-8").split())
             jc = (1 - float(len(s1.intersection(s2))) / float(len(s1.union(s2))))
             #print jc
             if jc < maxjc:
                maxjc = jc
                headlinel = c  
        c += 1
    #print headlinel
    ps = ps[headlinel+2].strip()    
    f = open("headlinesentiment.txt","a")
    print ("Sentiment predicted through previous headlines: "+ ps)
    f.write(article.title.encode("utf-8"))
    f.write("\n")
    f.write(ps)
    f.write("\n")
    f.close()

        
    keywords = article.keywords


    rake_object_title = rake.Rake("SmartStoplist.txt")
    rake_object_html = rake.Rake("SmartStoplist.txt", 5, 3, 2)
    rake_object_summary = rake.Rake("SmartStoplist.txt", 5, 3, 2)
    title_keys = rake_object_title.run(article.title)
    keywords_html = rake_object_html.run(text)
    keywords_summary = rake_object_summary.run(article.summary)
    
    #print keyword
    count = 0
    #for i in range(len(keywords_html)):
    #    keywords.append(keywords_html[i][0])
    #    count = count + 1
    #    if count > 4:
    #        break
    
    #for i in range(len(title_keys)):
    #    keywords.append(title_keys[i][0])
    
    #for i in range(len(keywords_summary)):
     #   keywords.append(keywords_summary[i][0])
    keywords = l 
    for i in range(len(keywords)):  
      
        #keywords[i] = keywords[i].encode("utf-8")
        keywords[i] = re.sub('[^A-Za-z0-9\s]+', '', keywords[i])
    if "reading" in keywords:
        keywords.remove("reading")
    #print(keywords)
    

    CONSUMER_KEY = "5k315aJtfEpZOftsOpOIPrvai"
    CONSUMER_SERCRET = "wicLMZQQGnQi7oqMYCZVJyRNilz29PMZQSHDetKM4i8fIUfkZv"
    ACCESS_TOKEN = "65937816-xVJP9P4oVbBbJkVs1Sarq7N2sqRI8WKGY9HG5Igzm"
    ACCESS_TOKEN_SECRET = "HlorBQc8xaKXq1KdUirQx90eIBLofkilBNvbUOid83K9R"
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SERCRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    myStream.filter(languages=["en"],track=keywords)

    #keystostring = " ".join(keywords)
    #keystostring = '"' + re.sub('\s', '","', keystostring) + '"'
    #print(keystostring)
    #myStream.filter(track=["apple"])

    '''with open('tweets.json', 'r') as f:
        for line in f:
            tweet = json.loads(line)['text']
            terms_stop = [term for term in preprocess(tweet) if term not in stop]
    
    print(terms_stop)'''
tw = []
t = ""

count = 0
with open('tweets.txt') as f:
    for line in f:
        if line.strip() == "##########":
            #print "ss"
            for key in keywords:
                if(key in t.split()):
                    count = count + 1
            if count >= 4:
                    tw.append(t)
                    #print t
                    t = ""
                    count = 0
            t = ""
        else:
            t = t + line
    #tw = f.readlines()

tw = [x.strip() for x in tw]
#for t in tw:
#    print t
#    print "\n"
sentiment.main(tw)
