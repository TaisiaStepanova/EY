from lub import *

class Controller:
    def __init__(self):
        super().__init__()

    def setView(self, view):
        self.view = view

    def get_data(self):
        dict = []
        dict2 = read_dict()
        print(dict2)
        for i in dict2:
            dict.append(i['start_form'])
        return dict


    def search_data(self, filter):
        data = find_in_dict(read_dict(), filter)
        if data == None:
            return []
        return [data['start_form']]

    def del_word(self, word):
        new_dict = delete_from_dict(read_dict(), str(word.id))
        save_dict(new_dict)
        self.view.show_data('nan')


    def view_word(self, event):
        pass

    def selected(self, filename, label, button):
        if filename[0].find('docx', -4) == -1:
            label.text = 'Выберите docs файл!'
            button.disabled = True
        else:
            label.text = ''
            self.file = filename[0]
            button.disabled = False

    def load_word(self, label, button=None):
        update_dict(self.file)
        print(self.file)
        button.disabled = True
        label.text = 'Загружено'
        self.view.show_data('nan')


    def get_forms(self, word):
        return check_for_form(read_dict(), word)

    def get_form_n(self, word):
        dict = []
        tmp = define_part(word)
        dict.append(tmp['part'])
        dict.append(tmp['base'])
        dict.append(tmp['start_form'])
        return dict

    def edit_form(self, new_form, label):
        dict = read_dict()
        new_dict = change_word_form(dict, self.view.word, self.view.form, new_form.text)
        save_dict(new_dict)
        label.text = 'Изменено'
        self.view.show_data_form(self.view.word)

    def gen_noun(self, id, start_form):
        if start_form.text == " ":
            id.text = 'Начальная форма не указана'
        else:
            filter = self.view.set_noun[0] + self.view.set_noun[1]
            tmp_form = generate_word_form(read_dict(), start_form.text.replace(' ', ''), filter)
            if tmp_form == None:
                id.text = 'Несуществующая форма'
            else:
                id.text = tmp_form

    def gen_adj(self, id, start_form):
        if start_form.text == " ":
            id.text = 'Начальная форма не указана'
        else:
            filter = self.view.set_adj[0] + self.view.set_adj[1] + self.view.set_adj[2]
            tmp_form = generate_word_form(read_dict(), start_form.text.replace(' ', ''), filter)
            if tmp_form == None:
                id.text = 'Несуществующая форма'
            else:
                id.text = tmp_form

    def gen_verb(self, id, start_form):
        if start_form.text == " ":
            id.text = 'Начальная форма не указана'
        else:
            filter = self.view.set_verb[0] + self.view.set_verb[1] + self.view.set_verb[2] + self.view.set_verb[3]
            tmp_form = generate_word_form(read_dict(), start_form.text.replace(' ', ''), filter)
            id.text = tmp_form

