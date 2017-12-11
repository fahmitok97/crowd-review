import tweepy
import json
from auth import get_auth
from settings import NUM_CRAWLED
from whitelist import ADJECTIVE_SUPERLATIVE_MAP

def contain_whitelist(tweet):
	for word in tweet.split(' '):
		if word.lower() in ADJECTIVE_SUPERLATIVE_MAP:
			return True
	return False

def search_by_hashtag(hashtag):
	api = tweepy.API(get_auth())
	crawled = 0
	for status in tweepy.Cursor(api.search, q=hashtag, tweet_mode='extended', lang='en').items(3 * NUM_CRAWLED):

		if crawled == NUM_CRAWLED:
			break

		if status.full_text[:2] == 'RT':
			continue

		if not contain_whitelist(status.full_text):
			continue

		crawled += 1	

		with open('review.json') as f:
			tweets = json.load(f)

		tweets.append(status.full_text)

		with open('review.json', 'w') as f:
			json.dump(tweets, f)

search_by_hashtag('#coco')
search_by_hashtag('#justiceleague')
search_by_hashtag('#wonderthemovie')
search_by_hashtag('#daddyshome2')
search_by_hashtag('#thorragnarok')
search_by_hashtag('#murderontheorientexpress')
search_by_hashtag('#starmovie')
search_by_hashtag('#ladybird')
search_by_hashtag('#threebillboards')
search_by_hashtag('#badmomsxmas')
search_by_hashtag('#jigsaw')
search_by_hashtag('#itmovie')
search_by_hashtag('#despicableme3')
search_by_hashtag('#geostorm')
search_by_hashtag('#theforeigner')
search_by_hashtag('#happydeathday')
search_by_hashtag('#kingsmanthegoldencircle')