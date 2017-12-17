import json
from tweepy import OAuthHandler, Cursor, API

from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, NUM_CRAWLED
from whitelist import ADJECTIVE_SUPERLATIVE_MAP

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_secret = ACCESS_SECRET

class Fetcher():

	def __init__(self, with_access_token=False):
		self.auth = OAuthHandler(consumer_key, consumer_secret)

		if with_access_token:
			self.auth.set_access_token(access_token, access_secret)

		self.api = API(self.auth)

	def __contain_whitelist(self, tweet):
		for word in tweet.split(' '):
			if word.lower() in ADJECTIVE_SUPERLATIVE_MAP:
				return True
		return False

	def search_by_hashtag(self, hashtag):
		crawled = 0
		tweets = []

		for status in Cursor(self.api.search, q=hashtag, tweet_mode='extended', lang='en').items(3 * NUM_CRAWLED):

			if crawled == NUM_CRAWLED:
				break

			if status.full_text[:2] == 'RT':
				continue

			if not self.__contain_whitelist(status.full_text):
				continue

			crawled += 1

			tweets.append(status.full_text)

		return tweets
