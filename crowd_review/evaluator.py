class Evaluator():
	def mean_average_precision(model_tweets, tweet_results):
		"""Calculate MAP comparing model_tweets with tweet_results
		Params:
			model_tweets, tweet_results
			Type : list of list of tweets
				ex: [
					[
						"shark shark",
						"sharknado go"
					],
					[
						"coco royok",
						"cocokroyok"
					]
				]

		"""
		result = 0.0
		for i in range(min(len(model_tweets), len(tweets))):
			result += average_precision(model_tweets[i], tweets[i])

		return result / len(tweet_results)

	def average_precision(model_tweets, tweets):
		relevant_count = 0
		cumulative_precision = 0.0
		for i in range(min(len(tweets), len(model_tweets))):
			if tweets[i] == model_tweets[i]:
				relevant_count = relevant_count + 1
				cumulative_precision += relevant_count / (i + 1)

		return cumulative_precision / relevant_count
