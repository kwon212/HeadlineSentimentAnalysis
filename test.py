#So Yon Kwon
#Hw2
import re
import json
import random
from numpy.random import choice
from collections import defaultdict
class TweetsClustering:
    
    def __init__(self, k, d):
        self.k = k
	self.dataset = d
	self.parsedTweets = []
        self.tweets = {}
        self.jaccard = defaultdict(dict)
        self.seeds = list()
        self.clusters = defaultdict(set)
        self.centroids = dict()
        self.clustersprev = defaultdict(set)
    def preprocessSeeds(self):
        t = open("InitialSeeds.txt")
        self.seeds = [int(line.strip(',\n')) for line in t.readlines()]

        t.close()
    def setClusterNum(self,k):
	self.k = k
    def preprocessTweet(self):
        count = 0
        with open(self.dataset) as f:
            for tweet in f:
                parsed_tweet = {}

                tweet = tweet.replace(','," ",1)
                tweet = self.clean_tweet(tweet)
                tweet = tweet.split()
		
                #tweettxt = ' '.join(tweet[1::]).strip().decode(('utf-8'))
                if (len(tweet[1::])) > 0:
			#self.parsedTweets.append(tweet[1::])
			parsed_tweet['text'] = ' '.join(tweet[1::])
                	# saving sentiment of tweet
                	parsed_tweet['sentiment'] = tweet[0]
                	parsed_tweet['id'] = count
			self.parsedTweets.append(parsed_tweet) 
		
                	self.tweets[count] = tweet[1::]
                	#print("count: ", count, " tweet: ", tweet[1::])
			count = count + 1
		
                if count >= 5000:
                    return

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

    def getJaccard(self):
        for t1 in self.tweets:
            for t2 in self.tweets:
                s1 = set(self.tweets[t1])
                s2 = set(self.tweets[t2])
                self.jaccard[t1][t2] = 1 - float(len(s1.intersection(s2))) / float(len(s1.union(s2)))                
        #print (self.jaccard)
    
    def initializeClusters(self):
        for i in range(self.k):
            self.clusters[i] = set()
            self.centroids[i] = self.seeds[i]


    def convergeClusters(self):
        #while self.clusters


        #print (self.centroids)
        it = 0
        converge = False
        while not converge:
            it += 1
            self. clusters = defaultdict(set)
            for i in self.tweets:
                min = 2
                newk = 1
                for j in self.centroids:
                    if self.jaccard[i][self.centroids[j]] < min: 
                        min = self.jaccard[i][self.centroids[j]]
                    
                        newk = j
                #print (j)
                self.clusters[newk].add(i)
            #print (self.clusters)
            if self.clusters == self.clustersprev:
                converge = True
                #print("iteration " + str(it))
                test = 0
                '''for c in self.centroids:
                    
                    print (str(self.centroids[c])+":"),
                    #print ("data: " )
                    #print (self.clusters[c])
                    for ci in self.clusters[c]:
                        print (ci),
                        #test+=1
                    print("\n")
                    #print (test)'''
            self.getCentroids()
            self.clustersprev = self.clusters
        #print (self.centroids)
        #print (self.clusters)

    def getCentroids(self):
        for i in self.clusters:
            minsum = 0    
            for j in self.clusters[i]:
                minsum += self.jaccard[j][self.centroids[i]]  
            for j in self.clusters[i]:           
                sum = 0
                for k in self.clusters[i]:
                    sum += self.jaccard[j][k]
                if minsum > sum:
                    minsum = sum
                    self.centroids[i] = j

    def determineCentroids(self):
        tweetList = [j for j in self.tweets]
        initialPick = random.choice(tweetList)
        newSeeds = []
        distance = {}
        newSeeds.append(initialPick)
        while len(newSeeds) < self.k:
            for n in newSeeds: 
                for t in self.tweets:
                    if t not in distance or self.jaccard[t][n] < distance[t]:
                        distance[t] = self.jaccard[t][n]
        
            prob = {}
            sum = 0
            for t in distance:
                sum += distance[t]*distance[t]

            for t in distance:
                prob[t] = float(distance[t]*distance[t]) / float(sum)
            
            tw = prob.keys()
            probz = prob.values()
            #print (tw, probz)
            s = choice(tw, p=probz)
            newSeeds.append(s)
        self.seeds =newSeeds
        #print (newSeeds)
        #print (len(newSeeds))
                
                
        


                    
                     
'''if __name__ == "__main__":
    t = TweetsClustering(25)
    #if you want to run the extra credit part, uncomment t.determineCentroids
    # and comment out t.prerprocessSeeds()
    #t.preprocessSeeds()
    t.preprocessTweet()
    #print(t.tweets)
    t.getJaccard()    
    t.determineCentroids()
    t.initializeClusters()
    t.convergeClusters()'''
    

