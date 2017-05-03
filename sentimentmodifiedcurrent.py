import sys
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
#import svm
sys.path.append("./libsvm-3.22/python")
from svmutil import *
import collections
 
class TwitterClient(object):

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = "574nBqbQXyqr88FVSFTSBHdfm"
        consumer_secret = "smPvlO7kX9fkaYgc2eEeI0IPzvzljPSyqZD40Gg1YmWMXAtwco"
        access_token = "1010268331-X0EE9kF7nF32hrHjfkBOKzUcMducX1etEX4nj8g"
        access_token_secret = "mpF5xi7ObC8rLfG17ja0PixC597oDzQhB61tnETwaICjA"
        
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
 
    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        #areturn ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        #Convert to lower case
        tweet = tweet.lower()
        #Convert www.* or https?://* to URL
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
        #Convert @username to AT_USER
        tweet = re.sub('@[^\s]+','AT_USER',tweet)
        #Remove additional white spaces
        tweet = re.sub('[\s]+', ' ', tweet)
        #Replace #word with word
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        #trim
        tweet = tweet.strip('\'"')
        tweet = tweet.replace('"','')
        return tweet
 
    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and its Textblob sentiment.
        Note: this is only used to test accuracy of Textblob and not to build SVM
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            #fetched_tweets = self.api.search(q = query, count = count)
            f = open("src/sentimenttweets_random.txt",'r') 
            # parsing tweets one by one
            for tweet in f:
     
                parsed_tweet = {}

                tweet = tweet.replace(','," ",1)
                tweet = self.clean_tweet(tweet)
                tweet = tweet.split()

                tweettxt = ' '.join(tweet[1::]).strip().decode(('utf-8'))
                parsed_tweet['text'] = ' '.join(tweet[1::])
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = tweet[0]
                parsed_tweet['guesssentiment'] = self.get_tweet_sentiment(tweettxt)
 
                tweets.append(parsed_tweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def get_justtweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them. This is the
        function called to retrieve the sentiment tweets to train,test SVM. 
        '''
        # empty list to store parsed tweets
        tweets = []
        
        try:
            # call twitter api to fetch tweets
            f = open("src/sentimenttweets_random.txt",'r') 
            f = list(f)
            # parsing tweets one by one
            for tweet in f[:2000] :
                tweet = tweet.replace(','," ",1)

                tweet = self.clean_tweet(tweet)
                tweet = tweet.split()
                #print tweet
 
            # parsing tweets one by one
            #for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                #parsed_tweet = {}
 
                # saving text of tweet
               # parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                #parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
 
                # appending parsed tweet to tweets list
               # if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                #    if tweet.text not in tweets:
                #        tweets.append(tweet[0]+" "+tweet[1::])
                #else:
                tweets.append(tweet[0]+" "+' '.join(tweet[1::]))
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


    def replaceTwoOrMore(self,s):
        #look for 2 or more repetitions of character and replace with the character itself (like heyyy)
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        return pattern.sub(r"\1\1", s)

    def getStopWordList(self,stopWordListFileName):
        #read the stopwords file and build a list to filter out stopwords
        stopWords = []
        stopWords.append('AT_USER')
        stopWords.append('URL')

        fp = open(stopWordListFileName, 'r')
        line = fp.readline()
        while line:
            word = line.strip()
            stopWords.append(word)
            line = fp.readline()
        fp.close()
        return stopWords

    def getFeatureVector(self,tweet):
        """
        This is the function that builds the feature vector in the training stage.
        A feature vector, at this point (since we are dealing only with unigrams), is a 
        vector of sentiment related words (i.e words that have not been filtered out)
        The feature vector is what its used to predict sentiment in the testing stage.
        """
        #get stop words
        st = open('src/stopwords.txt', 'r')
        stopWords = self.getStopWordList('src/stopwords.txt')

        featureVector = []
        #split tweet into words
        words = tweet.split()
        for w in words:
            #replace two or more with two occurrences
            w = self.replaceTwoOrMore(w)
            #strip punctuation
            w = w.strip('\'"?,.')
            #check if the word stats with an alphabet
            val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
            #ignore if it is a stop word
            if(w in stopWords or val is None):
                continue
            else:
                featureVector.append(w.lower())
        return featureVector
    #end


    def getSVMFeatureVL(self, tweets, featureList):
        """
        This is where we check the feature vector against the tweet.
        Based on the tweet's classification(which is available from the dataset we have),
        we label the features with either a 0,1,2.
        """

        sortedFeatures = sorted(featureList)
        map = {}
        feature_vector = []
        labels = []
        for t in tweets:
            label = 0
            map = {}
            #Initialize empty map
            for w in sortedFeatures:
                map[w] = 0

            tweet_words = t[0]
            tweet_opinion = t[1]
            #Fill the map
            t = t.split(" ")
            tweet_opinion = t[0]
            #print tweet_opinion
            for word in t[1:]:
                #process the word (remove repetitions and punctuations)
                word = self.replaceTwoOrMore(word)
                word = word.strip('\'"?,.')
                #set map[word] to 1 if word exists
                if word in map:
                    map[word] = 1
            #end for loop
            values = map.values()
            feature_vector.append(values)
            if(tweet_opinion == 'positive'):
                label = 0
            elif(tweet_opinion == 'negative'):
                label = 1
            elif(tweet_opinion == 'neutral'):
                label = 2
            labels.append(label)
        #return the list of feature_vector and labels
        return {'feature_vector' : feature_vector, 'labels': labels}
    def getSVMFeatureVLT(self, tweets, featureList):
        """
        This is where we check the feature vector against the tweet.
        Based on the tweet's classification(which is available from the dataset we have),
        we label the features with either a 0,1,2.
        """

        sortedFeatures = sorted(featureList)
        map = {}
        feature_vector = []
        labels = []
        for t in tweets:
            label = 0
            map = {}
            #Initialize empty map
            for w in sortedFeatures:
                map[w] = 0

            #tweet_words = t[0]
            #tweet_opinion = t[1]
            #Fill the map
            t = t.split(" ")
            #tweet_opinion = t[0]
            #print tweet_opinion
            for word in t:
                #process the word (remove repetitions and punctuations)
                word = self.replaceTwoOrMore(word)
                word = word.strip('\'"?,.')
                #set map[word] to 1 if word exists
                if word in map:
                    map[word] = 1
            #end for loop
            values = map.values()
            feature_vector.append(values)
            #af(tweet_opinion == 'positive'):
            ##    label = 0
            #elif(tweet_opinion == 'negative'):
            ##    label = 1
            #elif(tweet_opinion == 'neutral'):
            #    label = 2
            labels.append(-1)
        #return the list of feature_vector and labels
        return {'feature_vector' : feature_vector, 'labels': labels}    
#end

#Train the classifier

def main(tweets):
    api = TwitterClient()

    """
    testing Textblob accuracy (has nothing to do with SVM)
    
    tweets = api.get_tweets(query = 'Trump', count = 10)
    #print tweets
iINES TERMINATED BY '\n';
    # picking positive tweets from tweets
    count = 0
    for tweet in tweets:
        if tweet['sentiment'] == tweet['guesssentiment']:
            count += 1
    print count
    # percentage of positive tweets
    #print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    print ("accuracy:"+str(float(count)/float(len(tweets))))
    # percentage of negative tweets
  #  print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    # percentage of neutral tweets
   # print("Neutral tweets percentage: {} % \
    #    ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
 
    # printing first 5 positive tweets
    # print("\n\nPositive tweets:")
    # for tweet in ptweets[:10]:
    #     print(tweet['text'])
 
    # # printing first 5 negative tweets
    # print("\n\nNegative tweets:")
    # for tweet in ntweets[:10]:
    #    print(tweet['text'])

    """
    """
    Training, testing SVM
    """
    train_tweets = api.get_justtweets(query = 'Trump', count = 10)
    #print (len(tweets))
    #split dataset into 60/40 train, test split
    #start = int(len(tweets)*0.60)
    #train_tweets = tweets[0:start]
    
    test_tweets = tweets
    print test_tweets
    #print len(train_tweets), len(test_tweets)
    fv = []

    #Train the classifier: expand feature vector from training set
    for t in tweets:
        
        featureVector = api.getFeatureVector(t)
        fv.extend([f for f in featureVector if f not in fv])
     
    """      
    result = api.getSVMFeatureVL(train_tweets, fv)
    print result['labels']
    problem = svm_problem(result['labels'], result['feature_vector'])

    param = svm_parameter('-q')
    param.kernel_type = LINEAR
    param.probability = 1
    #svm_save_model('classifierDumpFile',classifier)
   
    classifier = svm_train(problem, param)
    svm_save_model('classifierDumpFile', classifier)

    """
    classifier = svm_load_model('classifierDumpFile')
    #Test the classifier with the test set
    test_feature_vector = api.getSVMFeatureVLT(test_tweets, fv)
    p_labels, p_accs, p_vals = svm_predict(test_feature_vector['labels'],test_feature_vector['feature_vector'], classifier, "-b 1")
    #print p_labels
    #print p_accs
    #print p_vals
    c = collections.Counter(p_labels)
    print c
    pval = c.most_common(1)[0][0]
    print pval
    sum = 0
    for p in range(len(p_vals)):
        #get probability of belonging in that class
        if p_labels[p] == pval:
            sum  += p_vals[p][int(p_labels[p])]

    print sum
    sumavg = float(sum)/float(c.most_common(1)[0][1])
    print sumavg
        #print pval
    if int(pval) == int(0):
        sent = "positive"
    if int(pval) == int(1):
        sent = "negative"
    if int(pval) == int(2):
        sent = "neutral"

    f = open("headlinesentiment.txt","a")
    if sumavg > (float(0.75)):
        print "strongly",sent
        f.write("strongly "+sent)
    elif sumavg >= (0.25) and sumavg <= (0.75):
        f.write(sent)
        print sent
    else:
        f.write("midly "+sent)
        print "mildly", sent
    f.write("\n")
    f.close()

if __name__ == "__main__":
    # calling main function
    main()
