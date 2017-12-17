from ekphrasis.classes.preprocessor import TextPreProcessor
from ekphrasis.classes.tokenizer import SocialTokenizer
from ekphrasis.dicts.emoticons import emoticons
from nltk.stem.porter import PorterStemmer

from crowd_review.models.token import Token

EMOJI_MAPPER = {'😃': '<happy>'}

OMITTED_TOKEN = ['~', ',', '&', '"', '\'', '{', '}', '#', '@', '$', '%', '^', '*', '(', ')', '-', '_', '=', '[', ']', '|'
                '±', '§', '\\', '<', '>', '?', '/', '`', '.', '+', ':']

class PreProcessor():

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.text_processor = TextPreProcessor(
            normalize=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'number'],
            omit=['url', 'email', 'percent', 'money', 'phone', 'user', 'time', 'url', 'date', 'number'],
            annotate={'allcaps', 'elongated', 'repeated','emphasis'},

            segmenter="twitter",

            corrector="twitter",

            unpack_hashtags=True,
            unpack_contractions=True,
            spell_correct_elong=False,
            spell_correction=True,

            tokenizer=SocialTokenizer(lowercase=True).tokenize,

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
                prevToken = Token(context=elem, base_context=self.stemmer.stem(elem))

        tokens.append(prevToken)
        return tokens[1:]
