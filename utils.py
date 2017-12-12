from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.classes.segmenter import Segmenter

import json

# # @author = Anab
# def remove_special_character(tweet):
#     pass

# # @author = Aldi
# def remove_mention(tweet):
#     pass

# # @author = Ayaz
# def remove_hashtag(tweet):
#     #seg_tw = Segmenter(corpus="twitter")
#     tokens = tweet.token()
#     #return seg_tw.segment(tweet)
#     pass

# # @author = Aldi
# def separate_between_char_and_non_char(tweet):
#     pass

# # @author = Anab
# def to_lower(tweet):
#     pass

# # @author = Fahmi
# def normalize_slang(tweet):
#     pass

# # @author = Ayaz
# def filter_non_alphanumeric(tweet):
#     pass

# # @author = Fahmi
# def word_count(tweet):
#     pass

# def tokenize(tweet):
#     social_tokenizer = SocialTokenizer(lowercase=False).tokenize


# def preprocess_tweet(tweet):
#     tweet_tokens = tokenize(tweet)
#     tweet = remove_mention(tweet)
#     tweet = remove_hashtag(tweet)
#     tweet = separate_between_char_and_non_char(tweet)
#     tweet = to_lower(tweet)
#     tweet = normalize_slang(tweet)
#     tweet = filter_non_alphanumeric(tweet)

    # return tweet

class PreProcessor():

    def __init__(self):
        self.social_tokenizer = SocialTokenizer(lowercase=False).tokenize
        self.segmenter = Segmenter(corpus="twitter")

    def __tokenize(self, tweet):
        return self.social_tokenizer(tweet)

    def __expand_hashtag(self, tweet_tokens):
        return [ item for tweet_token in tweet_tokens for item in self.segmenter.segment(tweet_token).split(' ')]

    def process_doc(self, tweet):
        tweet_tokens = self.__tokenize(tweet)
        tweet_tokens = self.__expand_hashtag(tweet_tokens)
        return tweet_tokens

def main():
    pre_processor = PreProcessor()

    with open('review.json') as f:
            tweets = json.load(f)

    print(pre_processor.process_doc(tweets[0]))


main()