from utils import Token, PreProcessor
from app import senti_strength

pre_processor = PreProcessor()
senti = senti_strength.SentiStrength()

tweets = []
tweets.append('not very good movie, but i love it though')
tweets.append('very bad movie huh?')
tweets.append('very bad movie')
tweets.append('bad movie')
tweets.append('this movie is trash suck and really bad, but i REALLY LOVE IT!!!!')
tweets.append('this movie is trash suck and really bad, but i really love it')
tweets.append('good movie, but i don\'t love it')
tweets.append('bad movie, but i love it')

for tweet in tweets:
	print (tweet, senti.calculate_doc(pre_processor.process_doc(tweet)))