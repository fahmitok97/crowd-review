import math

K = 200
THRESHOLD = 10

class TfIdf():

    def __init__(self):
        self.tfs = {}
        self.idfs = {}

    def supply_collections(self, tweets):
        tweets_context = []
        for tweet in tweets:
            words = []
            for word in tweet:
                words.append(word.get_base_context())
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

    def __get_tf_idf(self, word):
        if word in self.idfs.keys():
            return self.tfs[word] * math.log2(self.document_size / self.idfs[word])
        return 0

    def get_weight(self, tweet):
        weight = 0
        words = {}

        for word in tweet:
            word_context = word.get_base_context()

            if word_context not in words.keys():
                words[word_context] = 1
                weight += self.__get_tf_idf(word_context)

        weight /= max(THRESHOLD, len(tweet))
        return weight

# tweets = [
#     ['lololol'],
#     ['aku', 'ganteng', 'sekali'],
#     ['hah', 'bau'],
#     ['sekali', 'aku', 'ganteng']
# ]

# print(get_k_topmost_tweet(tweets))