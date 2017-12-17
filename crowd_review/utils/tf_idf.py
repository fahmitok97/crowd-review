import math
from senti_strength 

K = 200
THRESHOLD = 10

# deprecated
def similiar(tweet1, tweet2):
    tf1 = {}
    tf2 = {}

    for word in tweet1:
        if word in tf1.keys():
            tf1[word] += 1
        else:
            tf1[word] = 1

    for word in tweet2:
        if word in tf2.keys():
            tf2[word] += 1
        else:
            tf2[word] = 1

    numerator = 0
    for word in tf1.keys():
        if word in tf2.keys():
            numerator += tf1[word] * tf2[word]

    denum1 = 0
    denum2 = 0

    for word in tf1.keys():
        denum1 += tf1[word] * tf1[word]
    for word in tf2.keys():
        denum2 += tf2[word] * tf2[word]

    denum = math.sqrt(denum1 * denum2)

    val = numerator / denum

    return 1 - abs(val) < 1e-9

# deprecated
def filter_similiar_tweet(tweets):
    filtered = []
    for i in range(len(tweets)):
        uniq = True

        for j in range(i+1, len(tweets)):
            if(similiar(tweets[i], tweets[j])):
                uniq = False
                break

        if uniq:
            filtered.append(tweets[i])
    return filtered

# deprecated
def get_k_topmost_tweet(tweets):
    tweets = filter_similiar_tweet(tweets)
    document_size = len(tweets)
    tfs = {}
    idfs = {}

    for tweet in tweets:
        words = {}

        for word in tweet:
            if word in tfs.keys():
                tfs[word] += 1
            else:
                tfs[word] = 1

            if word not in words.keys():
                words[word] = 1

                if word in idfs.keys():
                    idfs[word] += 1
                else:
                    idfs[word] = 1

    tweets.sort(key=lambda x: get_weight(document_size, tfs, idfs, x), reverse=True)

    return tweets

class TfIdf():

    def __init__(self, tweets):
        self.tfs = {}
        self.idfs = {}

        tweets_context = []
        for tweet in tweets:
            words = []
            for word in tweet.get_context():
                words.append(word)
            tweets_context.append(words)

        for tweet in tweets_context:
            words = {}

            for word in tweet:
                if word in self.tfs.keys():
                    self.tfs[word] += 1
                else:
                    self.tfs[word] = 1

                if word not in words.keys():
                    words[word] = 1

                    if word in self.idfs.keys():
                        self.idfs[word] += 1
                    else:
                        self.idfs[word] = 1

        self.document_size = len(tweets_context)

    def get_tf_idf(self, word):
        if word in self.idfs.keys():
            return self.tfs[word] * math.log2(self.document_size / self.idfs[word])
        return 0

    def get_weight(self, tweet):
        weight = 0
        words = {}

        for word in tweet:
            word_context = word.get_context()

            if word_context not in words.keys():
                words[word_context] = 1
                weight += self.get_tf_idf(word_context)

        weight /= max(THRESHOLD, len(tweet))
        return weight

# tweets = [
#     ['lololol'],
#     ['aku', 'ganteng', 'sekali'],
#     ['hah', 'bau'],
#     ['sekali', 'aku', 'ganteng']
# ]

# print(get_k_topmost_tweet(tweets))