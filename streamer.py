from tweepy import Stream
from tweepy.streaming import StreamListener
from auth import get_auth

class Streamer(StreamListener):

    def on_data(self, data):
        try:
            with open('review.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

twitter_stream = Stream(get_auth(), Streamer())
twitter_stream.filter(track=['#MovieReview', '#movieReview', '#moviewreview'])