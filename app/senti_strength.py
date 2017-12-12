import json

def open_json_file(directory):
    with open(directory) as json_data:
        json_data = json.load(json_data)
    return json_data

def find_word_from_dict(word, word_dict):
    # if no change needed
    if word in word_dict:
        return word, False

    # check more than 2 repeating characters
    # repeating index = [{start_index, end_index}]
    repeating_idxs = []

    start_idx = 0
    prev_char = word[0]
    cnt = 1

    for (current_idx, current_char) in enumerate(word):
        if current_idx == 0:
            continue 

        if current_char == prev_char:
            cnt += 1
        else:
            if cnt >= 3:
                repeating_idxs.append((start_idx, current_idx - 1))

            cnt = 1
            prev_char = current_char
            start_idx = current_idx

    if cnt >= 3:
        repeating_idxs.append((start_idx, current_idx - 1))


    # bruteforce all combination
    for bitmask in range(0, 2**len(repeating_idxs)):
        cur_bitmask = bitmask
        cur_word = word

        for i in range(0, len(repeating_idxs)):
            start_idx, end_idx = repeating_idxs[i]

            if cur_bitmask % 2 == 1:
                # take 2 chars
                cur_word = cur_word[:(start_idx+2)] + cur_word[(end_idx+1):]
            else:
                # take 
                cur_word = cur_word[:(start_idx+1)] + cur_word[(end_idx+1):]
                

            cur_bitmask /= 2

        if cur_word in word_dict:
            return cur_word, True

    return None, None

def senti_strength(words):
    # // https://github.com/hitesh915/sentimentstrength/blob/master/wordwithStrength.txt
    word_dict = open_json_file('../dicts/words.json')
    # https"://github.com/athanrous/PySentiment/blob/master/SentiStrength/SentStrength_Data/BoosterWordList.txt
    booster_word_dict = open_json_file('../dicts/booster_words.json')
    negating_word_dict = open_json_file('../dicts/negating_words.json')

    words_strength = []

    booster_score = 0
    current_strength = 0
    is_negating = False
    prev_word_from_dict = ""

    for word in words:
        if word in negating_word_dict:
            is_negating = True
            prev_word_from_dict = ""
        else if word in booster_word_dict:
            booster_score += booster_word_dict[word]
            prev_word_from_dict = ""
        else if word == '!':
            if prev_word_from_dict != "":
                words_strength[-1] += 1 if words_strength[-1] - 1e-9 > 0 else words_strength[-1] -= 1
            prev_word_from_dict = ""
        else if word == '?':
            if prev_word_from_dict != "":
                words_strength[-1] = 0
            prev_word_from_dict = ""
        else:
            word, is_repeating = find_word_from_dict(word, word_dict)

            if word is None:
                continue

            current_strength = word_dict[word]

            if is_repeating is True:
                current_strength += 1 if current_strength - 1e-9 > 0 else current_strength -= 1

            if prev_word_from_dict != "":
                polarity = current_strength * words_strength[-1]
                if polarity - 1e-9 > 0:
                    current_strength += 1 if current_strength - 1e-9 > 0 else current_strength -= 1

            if is_negating is True:
                current_strength *= -1

            booster_polarity = current_strength * booster_score

            if booster_polarity - 1e-9 < 0:
                booster_score *= -1

            current_strength += booster_score

            words_strength.append(current_strength)

            booster_score = 0
            is_negating = False
            prev_word_from_dict = word

    return min(words_strength), max(words_strength)
