class Evaluator():
	def mean_average_precision(model_tweets, tweet_results):
		result = 0.0
		for tweets in tweet_results:
			result += average_precision(model_tweets, tweets)

		return result / len(tweet_results)

	def average_precision(model_tweets, tweets):
		relevant_count = 0
		cumulative_precision = 0.0
		for i in range(min(len(tweets), len(model_tweets))):
			if tweets[i] == model_tweets[i]:
				relevant_count = relevant_count + 1
				cumulative_precision += relevant_count / (i + 1)

		return cumulative_precision / relevant_count
