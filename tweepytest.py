# whitney choo
# homework 1 example 3b

import tweepy
from tweepy.streaming import StreamListener

class MyStreamListener(StreamListener):
	
	
	def on_status(self, status):
		print(status.text)

	def on_error(self, status):
		print(status)

if __name__ == '__main__':
	CONSUMER_KEY = "5k315aJtfEpZOftsOpOIPrvai"
	CONSUMER_SERCRET = "wicLMZQQGnQi7oqMYCZVJyRNilz29PMZQSHDetKM4i8fIUfkZv"
	ACCESS_TOKEN = "65937816-xVJP9P4oVbBbJkVs1Sarq7N2sqRI8WKGY9HG5Igzm"
	ACCESS_TOKEN_SECRET = "HlorBQc8xaKXq1KdUirQx90eIBLofkilBNvbUOid83K9R"
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SERCRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

	myStream.filter(locations=[-86.33,41.63,-86.20,41.74])



