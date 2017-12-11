import json

def remove_special_character(tweet):
    # include remove newline, special character and unicode
    pass

def remove_mention(tweet):
    pass

def remove_hashtag(tweet):
    pass

def separate_between_char_and_non_char(tweet):
    pass

def to_lower(tweet):
    pass

def normalize_slang(tweet):
    pass

def filter_non_alphanumeric(tweet):
    pass

def word_count(tweet):
    # return length of words
    pass

def preprocess_tweet(tweet):
    tweet = remove_special_character(tweet)
    tweet = remove_mention(tweet)
    tweet = remove_hashtag(tweet)
    tweet = separate_between_char_and_non_char(tweet)
    tweet = to_lower(tweet)
    tweet = normalize_slang(tweet)
    tweet = filter_non_alphanumeric(tweet)

    return tweet

def main():
    with open('review.json') as f:
            tweets = json.load(f)

    prepocessed_tweet = []

    for tweet in tweets:
        prepocessed_tweet.append(preprocess_tweet(tweet))


main()