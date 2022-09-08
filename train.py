russian_letters = set(list("абвгдеёжзийклмнопрстуфцчшщъыьэюя"))
splitters = ["\n", ".", ",", "’", "!", "?", "*", "—", "–", "...", "'", "«", "»", ")", "(", ";", "}", ":", "{", "<", "'",
             ">", "!", "[", "|", "]", "/", "#", "^", "+", "=", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
             "@",
             "I", "V", "X", "ГЛАВА", "ТОМ", "ЧАСТЬ", "Р", "Стр"]


def file_to_words(file_name, splitters, rus_letters):
    tmp_txt = open(file_name, 'r', encoding="UTF-8")
    tmp_str = tmp_txt.read()

    # разбиваю строку на массив
    for spl in splitters:
        tmp_str = tmp_str.replace(spl, " ")

    tmp_str = tmp_str.split()

    # удаляю нерусские символы
    rus_words = []
    for word in tmp_str:
        word = word.lower()
        if (word[0] in russian_letters):  # привожу все слова к нижнему регистру и кладу в массив numpy все русский слова
            rus_words += [word]
    return rus_words


# ТРЕНИРУЮ МОДЕЛЬ И ОПИСЫВАЮ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
def find_in_list(your_dict, key_list, your_word):
    list_of_lists = your_dict[key_list]
    found_word = False

    for lst in list_of_lists:
        if (lst[0] == your_word):
            lst[1] += 1
            found_word = True
            break

    if (found_word == False):
        your_dict[key_list] += [[your_word, 1]]


def model_train(words, window_size):
    model = {'predict_len': window_size}
    words_cnt = len(words)

    for tmp_size in range(window_size):
        window_len = tmp_size + 2
        window = ['' for i in range(window_len)]

        for i in range(words_cnt - window_len + 1):
            for j in range(window_len):
                window[j] = words[i + j]
            # в этом месте заношу статистику в мой словарь
            if (model.get(tuple(window[:-1])) == None):
                model[tuple(window[:-1])] = [[window[-1:][0], 1]]
            else:
                find_in_list(model, tuple(window[:-1]), window[-1:][0])

    return model

import numpy as np
file_name = input()
#old_file_name = 'C:/texts/war_and_piece.txt'
words = file_to_words(file_name, splitters, russian_letters)

prefix_size = 2
model = model_train(words, prefix_size)
saved_file_name = input()
#old_saved_name = 'C:/texts/war_and_piece_model.npy'
np.save(saved_file_name, model)
