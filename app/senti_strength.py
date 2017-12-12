import json
import os

class SentiStrength():

    def __init__(self):
        # // https://github.com/hitesh915/sentimentstrength/blob/master/wordwithStrength.txt
        self.word_dict = self.__open_json_file('dicts/words.json')
        # https"://github.com/athanrous/PySentiment/blob/master/SentiStrength/SentStrength_Data/BoosterWordList.txt
        self.booster_word_dict = self.__open_json_file('dicts/booster_words.json')
        self.negating_word_dict = self.__open_json_file('dicts/negating_words.json')

    def __open_json_file(self, directory):
        with open(directory) as json_data:
            json_data = json.load(json_data)
        return json_data

    def __increase_strength(self, initial_strength, addition):
        final_strength = initial_strength + (addition if initial_strength - 1e-9 > 0 else addition * -1)
        return final_strength

    def __is_same_polarity(self, strength1, strength2):
        polarity = strength1 * strength2
        return polarity - 1e-9 > 0

    def calculate_doc(self, tokenize_words):
        words_strength = []

        booster_score = 0
        current_strength = 0
        is_negating = False
        prev_word_from_dict = ""

        for tokenize_word in tokenize_words:
            word = tokenize_word.get_context()
            props = tokenize_word.get_prop()

            if word in self.negating_word_dict:
                is_negating = True
                prev_word_from_dict = ''
            elif word in self.booster_word_dict:
                booster_score += self.booster_word_dict[word]
                prev_word_from_dict = ''
            elif word == '!':
                if prev_word_from_dict != '':
                    words_strength[-1] = self.__increase_strength(words_strength[-1], 1)
                prev_word_from_dict = ""
            elif word == '?':
                if prev_word_from_dict != '':
                    words_strength[-1] = 0
                prev_word_from_dict = ''
            else:
                if word not in self.word_dict:
                    continue

                current_strength = self.word_dict[word]

                for prop in props:
                    if prop == 'allcaps' or prop == 'elongated' or prop == 'emphasis':
                        current_strength = self.__increase_strength(current_strength, 1)

                if prev_word_from_dict != '':
                    if self.__is_same_polarity(current_strength, words_strength[-1]):
                        current_strength = self.__increase_strength(current_strength, 1)

                if is_negating is True:
                    current_strength *= -1

                if not self.__is_same_polarity(current_strength, booster_score):
                    booster_score *= -1

                current_strength += booster_score

                words_strength.append(current_strength)

                booster_score = 0
                is_negating = False
                prev_word_from_dict = word

        if not words_strength:
            return 0, 0

        return min(words_strength), max(words_strength)
