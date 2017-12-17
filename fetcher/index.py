import json

from settings import HASHTAGS
from fetcher import Fetcher

fetcher = Fetcher()
result = []
for hashtag in HASHTAGS:
	result.extend(fetcher.search_by_hashtag(hashtag))


with open('../review.json', 'w') as outfile:
    json.dump(result, outfile)

