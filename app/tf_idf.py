import math

K = 200
THRESHOLD = 10

def get_tf_idf(document_size, tfs, idfs, word):
    return tfs[word] * math.log2(document_size / idfs[word])

def get_weight(document_size, tfs, idfs, tweet):
    weight = 0
    words = {}

    for word in tweet:
        if word not in words.keys():
            words[word] = 1
            weight += get_tf_idf(document_size, tfs, idfs, word)

    weight /= max(THRESHOLD, len(tweets))
    return weight

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

# tweets = [
#     ['lololol'],
#     ['aku', 'ganteng', 'sekali'],
#     ['hah', 'bau'],
#     ['sekali', 'aku', 'ganteng']
# ]

# print(get_k_topmost_tweet(tweets))