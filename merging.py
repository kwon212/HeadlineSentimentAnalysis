#merge keyword parser and sentiment analyzer

import v1 as relevant
import sentimentmodified as sentiment
#from v1 import MyStreaListener
from v1 import mains
#from tweepy.streaming import StreamListener

#MyStreamListener.mains(StreamListener)


tweets = mains()
sentiment.main(tweets)




