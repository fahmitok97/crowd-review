import json
import time
import random
from tweepy import OAuthHandler, Cursor, API, TweepError

from fetcher.settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, NUM_CRAWLED
from fetcher.whitelist import ADJECTIVE_SUPERLATIVE_MAP

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

	def __filter_hashtag(self, tweet, hashtag):
		filtered_tweet = ''

		for token in tweet.split(' '):
			if token.lower() == hashtag:
				filtered_tweet += '***** '
			else:
				filtered_tweet += token + ' '

		return filtered_tweet

	def __exponential_backoff(self, backoff_time):
		time.sleep((2 ** backoff_time) + (random.randint(0, 1000) / 1000))
		return backoff_time + 1

	def search_by_hashtag(self, hashtag, with_id=False):
		crawled = 0
		tweets = []

		cursor = Cursor(self.api.search, q=hashtag, tweet_mode='extended', lang='en').items(3 * NUM_CRAWLED)

		next_backoff_time = 0

		while True:
			try:
				status = cursor.next()

				if crawled == NUM_CRAWLED:
					break

				if status.full_text[:2] == 'RT':
					continue

				if not self.__contain_whitelist(status.full_text):
					continue

				crawled += 1

				if with_id:
					tweets.append({'id': status.id_str, 'text': self.__filter_hashtag(status.full_text, hashtag)})
				else:
					tweets.append(self.__filter_hashtag(status.full_text, hashtag))

			except TweepError:
				next_backoff_time = self.__exponential_backoff(next_backoff_time)
				continue
			except StopIteration:
				break

		return tweets
