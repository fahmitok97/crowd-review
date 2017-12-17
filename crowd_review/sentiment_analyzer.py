from crowd_review.utils.senti_strength import SentiStrength
from crowd_review.utils.pre_processor import PreProcessor
from crowd_review.utils.tf_idf import TfIdf


class SentimentAnalyzer():

	@staticmethod
	def process(tweets):
		pre_processor = PreProcessor()
		senti_strength = SentiStrength()
		tf_idf = TfIdf()

		tokenized_tweets = []
		for tweet in tweets:
			tokenized_tweet = pre_processor.process_doc(tweet['text'])
			tokenized_tweets.append(tokenized_tweet)

			tweet['tokenized'] = tokenized_tweet
			_, _, tweet['senti_str'] = senti_strength.calculate_doc(tokenized_tweet)

		tf_idf.supply_collections(tokenized_tweets)
		for tweet in tweets:
			tweet['tf_idf'] = tf_idf.get_weight(tweet['tokenized'])

		tweets.sort(key=lambda tweet: -1.0 * tweet['senti_str'] * tweet['tf_idf'])
		top_positive_tweet = tweets[:10]
		tweets.sort(key=lambda tweet: tweet['senti_str'] * tweet['tf_idf'])
		top_negative_tweet = tweets[:10]

		return top_positive_tweet, top_negative_tweet
