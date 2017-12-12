from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons

import json

EMOJI_MAPPER = {'😃': '<happy>'}

OMITTED_TOKEN = ['~', ',', '&', '"', '\'', '{', '}', '#', '@', '$', '%', '^', '*', '(', ')', '-', '_', '=', '[', ']', '|'
                '±', '§', '\\', '<', '>', '?', '/', '`', '.', '+']

class Token():

        def __init__(self, context=''):
            self.context = context
            self.properties = []

        def add_prop(self, property):
            self.properties.append(property)

        def get_prop(self):
            return self.properties

        def get_context(self):
            return self.context

        def __repr__(self):
            return self.context + ' ' + ' '.join(self.properties)

class PreProcessor():

    def __init__(self):
        self.text_processor = TextPreProcessor(
            # terms that will be normalized
            normalize=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'number'],
            # omit after normalized
            omit=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'number'],
            # terms that will be annotated
            annotate={'allcaps', 'elongated', 'repeated','emphasis'},

            # corpus from which the word statistics are going to be used
            # for word segmentation
            segmenter="twitter",

            # corpus from which the word statistics are going to be used
            # for spell correction
            corrector="twitter",

            unpack_hashtags=True,  # perform word segmentation on hashtags
            unpack_contractions=True,  # Unpack contractions (can't -> can not)
            spell_correct_elong=False,  # spell correction for elongated words
            spell_correction=True,

            # select a tokenizer. You can use SocialTokenizer, or pass your own
            # the tokenizer, should take as input a string and return a list of tokens
            tokenizer=SocialTokenizer(lowercase=True).tokenize,

            # list of dictionaries, for replacing tokens extracted from the text,
            # with other expressions. You can pass more than one dictionaries.
            dicts=[emoticons, EMOJI_MAPPER]
        )

    def process_doc(self, tweet):
        tokenized_doc = self.text_processor.pre_process_doc(tweet)
        tokens = []
        prevToken = Token()

        for elem in tokenized_doc:
            if elem[0] == '<':
                prevToken.add_prop(elem[1:len(elem)-1])
            else:
                if prevToken.get_context() not in OMITTED_TOKEN:
                    tokens.append(prevToken)
                prevToken = Token(context=elem)

        tokens.append(prevToken)
        return tokens[1:]



pre_processor = PreProcessor()
with open('review.json') as f:
        tweets = json.load(f)

for tweet in tweets:
    print(pre_processor.process_doc(tweet))

