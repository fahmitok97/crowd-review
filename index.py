import tweepy
import json
from auth import get_auth

def search_by_hashtag(hashtag):
	api = tweepy.API(get_auth())
	for status in tweepy.Cursor(api.search, q=hashtag).items(3):

		with open('review.json') as f:
			tweets = json.load(f)

		tweets.append(status.text)

		with open('review.json', 'w') as f:
			json.dump(tweets, f)

search_by_hashtag('#movieReview')