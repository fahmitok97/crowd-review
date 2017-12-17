from crowd_review.utils.pre_processor import PreProcessor
from crowd_review.utils.senti_strength import SentiStrength

import json

pre_processor = PreProcessor()
senti_strength = SentiStrength()

with open('review.json') as f:
        tweets = json.load(f)

tokenized_tweets = []
for tweet in tweets:
    print(senti_strength.calculate_doc(pre_processor.process_doc(tweet)))
