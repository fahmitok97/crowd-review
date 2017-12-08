import tweepy
import json
from tweepy import OAuthHandler
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET, NUM_CRAWLED

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET
access_token = ACCESS_TOKEN
access_secret = ACCESS_SECRET

def get_auth(with_access_token=False):
	auth = OAuthHandler(consumer_key, consumer_secret)
	if with_access_token:
	 auth.set_access_token(access_token, access_secret)
	return auth