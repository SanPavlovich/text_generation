import numpy as np


def get_popular_words(list_of_lists, top_size):
    popular_words_cnt = 0
    words_cnt = len(list_of_lists)
    # делаю словарь, сортирую его и беру из него самые частовстречающиеся слова
    words_dict = {}
    for i in range(words_cnt):
        words_dict[list_of_lists[i][0]] = list_of_lists[i][1]

    sorted_dict = {}
    sorted_keys = sorted(words_dict, key=words_dict.get)
    for w in sorted_keys:
        sorted_dict[w] = words_dict[w]

    popular_words = []
    tp_size = top_size if words_cnt > top_size else words_cnt
    popular_words_list = list(sorted_dict.keys())

    for i in range(tp_size):
        popular_words += [popular_words_list[len(sorted_dict) - i - 1]]

    return popular_words


def model_predict(model, your_text, gen_words_cnt, randomization):
    gen_text = your_text
    gen_text = your_text.split()
    size = model.get('predict_len')

    for i in range(gen_words_cnt):
        window_size = size
        while (window_size > 0):
            window = gen_text[-(window_size):]

            if (model.get(tuple(window)) == None):
                if (window_size == 1):
                    return gen_text
                else:
                    # print('didnt find such sequence of words in text')
                    window_size -= 1
            else:
                np_probable_words = np.array(get_popular_words(model.get(tuple(window)), randomization))
                np_rand_word = np.random.choice(np_probable_words)

                # условие на то, чтобы текст не генерировал два одинаковых подряд идущих слова
                while ([np_rand_word] == gen_text[-1:] and (len(np_probable_words) > 1)):
                    np_rand_word = np.random.choice(np_probable_words)

                gen_text += [np_rand_word]
                break
    return gen_text


def words_to_str(word_list):
    gen_str = ''
    for i in word_list:
        gen_str += i
        gen_str += ' '
    return gen_str

file_name = input()
#old_file_name = 'C:/texts/war_and_piece_model.npy'
model = np.load(file_name, allow_pickle=True).item()
your_text = 'я каждый день'
gen_text_len = 30
randomization = 20

gen_text = model_predict(model, your_text, gen_text_len, randomization)
print(words_to_str(gen_text))
