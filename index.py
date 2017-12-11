import tweepy
import json
from auth import get_auth
from settings import NUM_CRAWLED

def search_by_hashtag(hashtag):
	api = tweepy.API(get_auth())
	crawled = 0
	for status in tweepy.Cursor(api.search, q=hashtag, tweet_mode='extended').items(3 * NUM_CRAWLED):

		if crawled == NUM_CRAWLED:
			break

		if status.full_text[:2] == 'RT':
			continue

		crawled += 1	

		with open('review.json') as f:
			tweets = json.load(f)

		tweets.append(status.full_text)

		with open('review.json', 'w') as f:
			json.dump(tweets, f)

search_by_hashtag('#dunkirk')
search_by_hashtag('#coco')
search_by_hashtag('#EmojiMovie')
search_by_hashtag('#ThorRagnarok')
search_by_hashtag('#justiceleague')
search_by_hashtag('#transformers')
search_by_hashtag('#cars2')
search_by_hashtag('#hoteltransylvania')
search_by_hashtag('#NYSM2')
search_by_hashtag('#traintobusan')
search_by_hashtag('#wonderwoman')
search_by_hashtag('#cultofchucky')
search_by_hashtag('#catwoman')
search_by_hashtag('#babadook')
search_by_hashtag('#moana')
search_by_hashtag('#thepurge')
search_by_hashtag('#GirlsTrip')
search_by_hashtag('#captainunderpants')
search_by_hashtag('#sharknado')
search_by_hashtag('#fiftyshadesdarker')