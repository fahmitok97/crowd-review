from crowd_review.utils.pre_processor import PreProcessor
from crowd_review.utils.senti_strength import SentiStrength
from crowd_review.utils.tf_idf import TfIdf

import json

pre_processor = PreProcessor()
senti_strength = SentiStrength()
tf_idf = TfIdf()

with open('review.json') as f:
        tweets = json.load(f)


tokenized_tweets = []
for tweet in tweets:
    tokenized_tweet = pre_processor.process_doc(tweet)
    tokenized_tweets.append(tokenized_tweet)
    print(tokenized_tweet)
    print(senti_strength.calculate_doc(tokenized_tweet))

tf_idf.supply_collections(tokenized_tweets)
for tokenized_tweet in tokenized_tweets:
	print(tf_idf.get_weight(tokenized_tweet))

