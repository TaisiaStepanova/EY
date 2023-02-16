import pymorphy2
import docx
import json

all_cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
all_pers = ['1per', '2per', '3per']
all_numbers = ['sing', 'plur']
all_genders = ['masc', 'femn', 'neut']
all_tens = ['pres', 'past', 'futr']


def find_base(array):
    base = ''
    check = False
    max_base_size = len(array[0])
    for k in range(len(array)):
        if len(array[k]) < max_base_size:
            max_base_size = len(array[k])
    for i in range(max_base_size):
        for j in range(len(array) - 1):
            if array[j][i] == array[j + 1][i]:
                continue
            else:
                check = True
        if check == False:
            base = base + array[0][i]
    return base


def delete_base(base, array):
    for i in range(len(array)):
        array[i] = array[i][-(len(array[i]) - len(base)):]
        if array[i] == base:
            array[i] = ""
    return array


def create_matrix_of_verb():
    matrix_of_forms = []
    for i in range(3):
        times = []
        matrix_of_forms.append(times)
        for j in range(4):
            pers = []
            times.append(pers)
            for k in range(4):
                genders = [None, None]
                pers.append(genders)
    # print(matrix_of_forms)
    return matrix_of_forms


def create_matrix_noun():
    matrix_of_forms = []
    for i in range(6):
        cases = [None, None]
        matrix_of_forms.append(cases)
    return matrix_of_forms


def create_matrix_adjective():
    matrix_of_forms = []
    for i in range(6):
        cases = []
        matrix_of_forms.append(cases)
        for j in range(4):
            genders = [None, None]
            cases.append(genders)
    return matrix_of_forms


def create_matrix_noun():
    matrix_of_forms = []
    for i in range(6):
        cases = [None, None]
        matrix_of_forms.append(cases)
    return matrix_of_forms


def fill_matrix_noun(forms):
    matrix = create_matrix_noun()
    for i in range(6):
        matrix[i][0] = forms[2 * i]
        matrix[i][1] = forms[2 * i + 1]
    return matrix


def print_forms_noun(list_forms):
    list_pad = ['И.п.', 'Р.п.', 'Д.п.', 'В.п.', 'Т.п.', 'П.п.']
    list_1 = ['ед.ч.', 'мн.ч']
    word = []
    for i in range(len(list_forms)):
        for j in range(2):
            if list_forms[i][j] != None:
                word.append([list_pad[i] + ", " + list_1[j], list_forms[i][j]])
    return word


def print_forms_adj(list_forms):
    list_pad = ['И.п.', 'Р.п.', 'Д.п.', 'В.п.', 'Т.п.', 'П.п.']
    list_rod = ['м.р.', 'ж.р.', 'ср.р.', ' ']
    list_1 = ['ед.ч.', 'мн.ч']
    word = []
    for i in range(len(list_forms)):
        for j in range(4):
            for k in range(2):
                if list_forms[i][j][k] != None:
                    word.append([list_pad[i] + list_rod[j] + list_1[k], list_forms[i][j]])
    return word


def print_forms_verb(list_forms):
    list_t = ['пр.вр.', 'наст.вр.', 'буд.вр.']
    list_l = ['1.л.', '2.л.', '3.л.', 'н.л.']
    list_rod = ['м.р.', 'ж.р.', 'ср.р.', ' ']
    list_1 = ['ед.ч.', 'мн.ч']
    word = []
    for i in range(len(list_forms)):
        for j in range(4):
            for k in range(4):
                for q in range(2):
                    if list_forms[i][j][k][q] != None:
                        word.append([list_t[i] + list_l[j] + list_rod[k] + list_1[q], list_forms[i][j][k][q]])
    return word


def check_for_form(main_dict, our_word):
    our_dict = find_in_dict(main_dict, our_word)
    if our_dict['part'] == 'NOUN':
        return print_forms_noun(our_dict['forms'])
    if our_dict['part'] == 'VERB':
        return print_forms_verb(our_dict['forms'])
    if our_dict['part'] == 'ADJECTIVE':
        return print_forms_adj(our_dict['forms'])


def generate_word_form(main_dict, begin_form, string):
    print(string)
    our_dict = find_in_dict(main_dict, begin_form)
    if our_dict == None:
        return 'нет слова в словаре'
    count = 0
    for i in range(len(main_dict)):
        if main_dict[i] == our_dict:
            count = i
    if our_dict['part'] == 'NOUN':
        return generate_forms_noun(main_dict, string, count)
    if our_dict['part'] == 'VERB':
        return generate_forms_verb(main_dict, string, count)
    if our_dict['part'] == 'ADJECTIVE':
        return generate_forms_adj(main_dict, string, count)


def generate_forms_adj(main_dict, string, count):
    list_pad = ['И.п.', 'Р.п.', 'Д.п.', 'В.п.', 'Т.п.', 'П.п.']
    list_rod = ['м.р.', 'ж.р.', 'ср.р.', ' ']
    list_1 = ['ед.ч.', 'мн.ч.']
    if list_1[1] in string and list_rod[3] not in string:
        return 'несуществующая форма'
    for i in range(6):
        for j in range(4):
            for k in range(2):
                if list_pad[i] in string and list_rod[j] in string and list_1[k] in string:
                    print(list_rod[j])
                    finish_form = main_dict[count]['base'] + main_dict[count]['forms'][i][j]
                    return finish_form
    for i in range(6):
        for k in range(2):
            if list_pad[i] in string and list_1[k] in string:
                finish_form = main_dict[count]['base'] + main_dict[count]['forms'][i][3]
                return finish_form


def generate_forms_noun(main_dict, string, count):
    list_pad = ['И.п.', 'Р.п.', 'Д.п.', 'В.п.', 'Т.п.', 'П.п.']
    list_1 = ['ед.ч.', 'мн.ч']
    for i in range(6):
        for j in range(2):
            if list_pad[i] in string and list_1[j] in string:
                finish_form = main_dict[count]['base'] + main_dict[count]['forms'][i][j]
                return finish_form

def generate_forms_verb(main_dict, string, count):
    list_t = ['пр.вр.', 'наст.вр.', 'буд.вр.']
    list_l = ['1.л.', '2.л.', '3.л.', 'н.л.']
    list_rod = ['м.р.', 'ж.р.', 'ср.р.', ' ']
    list_1 = ['ед.ч.', 'мн.ч.']

    for i in range(3):
        for j in range(4):
            for k in range(4):
                for q in range(2):
                    if main_dict[count]['forms'][i][j][k][q] != None:
                        print(main_dict[count]['forms'][i][j][k][q])
                        if list_t[i] in string and list_l[j] in string and list_rod[k] in string and list_1[
                            q] in string:
                            finish_form = main_dict[count]['base'] + main_dict[count]['forms'][i][j][k][q]
                            print('n')
                            return finish_form

    return 'Несуществующая форма'

def change_word_form(main_dict, begin_form, string, finish_form):
    our_dict = find_in_dict(main_dict, begin_form)
    print(our_dict)
    count = 0
    for i in range(len(main_dict)):
        if main_dict[i] == our_dict:
            count = i
    print(i)
    if our_dict['part'] == 'NOUN':
        return change_forms_noun(main_dict, string, finish_form, count)
    if our_dict['part'] == 'VERB':
        return change_forms_verb(main_dict, string, finish_form, count)
    if our_dict['part'] == 'ADJECTIVE':
        return change_forms_adj(main_dict, string, finish_form, count)


def change_forms_verb(main_dict, string, finish_form, count):
    print(main_dict)
    print(string)
    list_t = ['пр.вр.', 'наст.вр.', 'буд.вр.']
    list_l = ['1.л.', '2.л.', '3.л.', 'н.л.']
    list_rod = ['м.р.', 'ж.р.', 'ср.р.', ' ']
    list_1 = ['ед.ч.', 'мн.ч.']
    for i in range(3):
        for j in range(4):
            for k in range(4):
                for q in range(2):
                    if list_t[i] in string and list_l[j] in string and list_rod[k] in string and list_1[q] in string:
                        print(main_dict[count]['forms'][i][j][k][q], 'hhhhh')
                        main_dict[count]['forms'][i][j][k][q] = finish_form
                        print(main_dict[count]['forms'][i][j][k][q], 'change')
                        return main_dict



def change_forms_adj(main_dict, string, finish_form, count):
    list_pad = ['И.п.', 'Р.п.', 'Д.п.', 'В.п.', 'Т.п.', 'П.п.']
    list_rod = ['м.р.', 'ж.р.', 'ср.р.', ' ']
    list_1 = ['ед.ч.', 'мн.ч']
    for i in range(6):
        for j in range(4):
            for k in range(2):
                if list_pad[i] in string and list_rod[j] in string and list_1[k] in string:
                    print(main_dict[count]['forms'][i][j], 'hhhhh')
                    main_dict[count]['forms'][i][j] = finish_form
                    print(main_dict[count]['forms'][i][j], 'change')
                    return main_dict


def change_forms_noun(main_dict, string, finish_form, count):
    list_pad = ['И.п.', 'Р.п.', 'Д.п.', 'В.п.', 'Т.п.', 'П.п.']
    list_1 = ['ед.ч.', 'мн.ч']
    for i in range(6):
        for j in range(2):
            if list_pad[i] in string and list_1[j] in string:
                main_dict[count]['forms'][i][j] = finish_form
                print(main_dict[count])
                return main_dict


def fill_matrix_adjective(forms):
    matrix = create_matrix_adjective()
    for i in range(6):
        matrix[i][3] = forms[4 * i]
        matrix[i][0] = forms[4 * i + 1]
        matrix[i][1] = forms[4 * i + 2]
        matrix[i][2] = forms[4 * i + 3]

    return matrix


def fill_matrix_verb(forms):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(forms[0])[0]
    matrix = create_matrix_of_verb()
    if 'perf' in word.tag:
        for i in range(3):
            matrix[0][i][0][0] = forms[0]
            matrix[0][i][1][0] = forms[1]
            matrix[0][i][2][0] = forms[2]
            matrix[0][i][3][1] = forms[3]
        matrix[2][0][3][0] = forms[4]
        matrix[2][0][3][1] = forms[5]
        matrix[2][1][3][0] = forms[6]
        matrix[2][1][3][1] = forms[7]
        matrix[2][2][3][0] = forms[8]
        matrix[2][2][3][1] = forms[9]
    else:
        matrix[0][3][0][0] = forms[0]
        matrix[0][3][1][0] = forms[1]
        matrix[0][3][2][0] = forms[2]
        matrix[0][3][3][1] = forms[3]
        matrix[1][0][3][0] = forms[4]
        matrix[1][0][3][1] = forms[5]
        matrix[1][1][3][0] = forms[6]
        matrix[1][1][3][1] = forms[7]
        matrix[1][2][3][0] = forms[8]
        matrix[1][2][3][1] = forms[9]
    return matrix


def change_noun(word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0]
    list_of_forms = []
    for case in all_cases:
        for number in all_numbers:
            list_of_forms.append(word.inflect({number, case}).word)
    return list_of_forms


def change_adjective(word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0]
    list_of_forms = []
    for case in all_cases:
        list_of_forms.append(word.inflect({'plur', case}).word)
        for gender in all_genders:
            list_of_forms.append(word.inflect({'sing', case, gender}).word)

    return list_of_forms


def change_verb(word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(word)[0]
    list_of_forms = []
    if 'perf' in word.tag:
        for gender in all_genders:
            list_of_forms.append(word.inflect({'past', gender, 'sing'}).word)
        list_of_forms.append(word.inflect({'past', 'plur'}).word)
        for per in all_pers:
            for number in all_numbers:
                list_of_forms.append(word.inflect({'futr', per, number}).word)
    else:
        for gender in all_genders:
            list_of_forms.append(word.inflect({'past', gender, 'sing'}).word)
        list_of_forms.append(word.inflect({'past', 'plur'}).word)
        for per in all_pers:
            for number in all_numbers:
                list_of_forms.append(word.inflect({'pres', per, number}).word)
    # print(list_of_forms)
    return list_of_forms


def for_chamge(our_word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(our_word)[0]
    if 'NOUN' in word.tag:
        list_of_forms = change_noun(our_word)
    elif 'VERB' in word.tag or 'INFN' in word.tag:
        list_of_forms = change_verb(our_word)
    elif 'ADJF' in word.tag:
        list_of_forms = change_adjective(our_word)
    return list_of_forms


def define_part_2(our_word):
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(our_word)[0]
    if 'NOUN' in word.tag:
        dict = {'start_form': word.normal_form, 'part': 'NOUN', 'forms': fill_matrix_noun(change_noun(our_word))}
    elif 'VERB' in word.tag:
        dict = {'start_form': word.normal_form, 'part': 'VERB', 'forms': fill_matrix_verb(change_verb(our_word))}
    elif 'ADJF' in word.tag:
        dict = {'start_form': word.normal_form, 'part': 'ADJECTIVE',
                'forms': fill_matrix_adjective(change_adjective(our_word))}
    return dict


def define_part(our_word):  # теперь 'forms' хранит все окончания
    morph = pymorphy2.MorphAnalyzer()
    word = morph.parse(our_word)[0]
    if 'NOUN' in word.tag:
        dict = {'start_form': word.normal_form, 'part': 'NOUN', 'base': find_base(change_noun(our_word)),
                'forms': fill_matrix_noun(delete_base(find_base(change_noun(our_word)), change_noun(our_word)))}
    elif 'VERB' in word.tag or 'INFN' in word.tag:
        dict = {'start_form': word.normal_form, 'part': 'VERB', 'base': find_base(change_verb(our_word)),
                'forms': fill_matrix_verb(delete_base(find_base(change_verb(our_word)), change_verb(our_word)))}
    elif 'ADJF' in word.tag:
        dict = {'start_form': word.normal_form, 'part': 'ADJECTIVE', 'base': find_base(change_adjective(our_word)),
                'forms': fill_matrix_adjective(
                    delete_base(find_base(change_adjective(our_word)), change_adjective(our_word)))}
    return dict


def delete_from_dict(main_dict, our_word):  # удалить из словаря по плову
    our_dict = define_part(our_word)
    for i in range(len(main_dict)):
        if main_dict[i]['start_form'] == our_dict['start_form']:
            main_dict.pop(i)
            return main_dict


def sort_main_dict(main_dict):  # сортировка словаря по алфавиту
    sorted_list = []
    sorted_dict = []
    for i in range(len(main_dict)):
        sorted_list.append(main_dict[i]['start_form'])
    sorted_list = sorted(sorted_list)
    for i in range(len(sorted_list)):
        morph = pymorphy2.MorphAnalyzer()
        new_word = morph.parse(sorted_list[i])[0]
        if 'NOUN' in new_word.tag or 'VERB' in new_word.tag or 'ADJF' in new_word.tag or 'INFN' in new_word.tag:
            sorted_dict.append(define_part(sorted_list[i]))
    return sorted_dict


def find_in_dict(main_dict, our_word):  # найти в словаре
    print(main_dict)
    our_dict = define_part(our_word)
    for i in range(len(main_dict)):
        if main_dict[i]['start_form'] == our_dict['start_form']:
            return main_dict[i]
    print("слово в словаре не найдено")
    return None


def add_to_main_dict(main_dict, our_word):  # довавить слова в ловарь, если уже есть такое-  не добавиться
    our_dict = define_part(our_word)
    for i in range(len(main_dict)):
        if main_dict[i]['start_form'] == our_dict['start_form']:
            return main_dict
    main_dict.append(our_dict)
    return main_dict


def read_from_doc(doc_name):  # с docx считать все обзацы
    doc = docx.Document(doc_name)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return text


def parse_doc(text):  # считанные обзацы разбить на слова, игнорируя запятые, точки и некоторые союзы типо на и

    words_list = []
    for i in range(len(text)):
        word = []
        for j in range(len(text[i])):
            if text[i][j] == " " or text[i][j] == "," or text[i][j] == ".":
                string = ''.join(word)
                if len(string) > 2:
                    morph = pymorphy2.MorphAnalyzer()
                    new_word = morph.parse(string)[0]
                    if 'NOUN' in new_word.tag or 'VERB' in new_word.tag or 'ADJF' in new_word.tag:
                        words_list.append(string)
                word.clear()
            else:
                word.append(text[i][j])
    print(words_list)
    return words_list


def save_dict(data):  # храним в json, надеюсь так можно
    with open('dict.json', 'w') as file:
        json.dump(data, file)


def read_dict():
    with open('dict.json', 'r') as file:
        dict = json.load(file)
        return dict


def analize_text(main_dict, text):
    for i in range(len(text)):
        if len(main_dict) == 0:
            main_dict.append(text[i])
        main_dict = add_to_main_dict(main_dict, text[i])
    main_dict = sort_main_dict(main_dict)
    return main_dict


def delete_from_dict(main_dict, our_word):
    our_dict = define_part(our_word)
    for i in range(len(main_dict)):
        if main_dict[i]['start_form'] == our_dict['start_form']:
            main_dict.remove(main_dict[i])
            return main_dict


def update_dict(file):
    main_dict = read_dict()
    text = parse_doc(read_from_doc(file))
    rezult_dict = analize_text(main_dict, text)
    save_dict(rezult_dict)
    return rezult_dict


if __name__ == '__main__':
    main_dict = read_dict()
    # text = parse_doc(read_from_doc('first_text.docx'))
    # rezult_dict = analize_text(main_dict,text)
    # print(check_for_form(main_dict,'подходящий'))
    print(generate_word_form(main_dict, 'страдать', 'пр.вр.,ед.ч.'))

# save_dict(rezult_dict)

