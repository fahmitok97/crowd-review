import json

# @author = Anab
def remove_special_character(tweet):
    pass

# @author = Aldi
def remove_mention(tweet):
    pass

# @author = Ayaz
def remove_hashtag(tweet):
    pass

# @author = Aldi
def separate_between_char_and_non_char(tweet):
    pass

# @author = Anab
def to_lower(tweet):
    pass

# @author = Fahmi
def normalize_slang(tweet):
    pass

# @author = Ayaz
def filter_non_alphanumeric(tweet):
    pass

# @author = Fahmi
def word_count(tweet):
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