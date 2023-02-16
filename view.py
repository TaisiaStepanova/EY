from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.label import Label
from kivymd.uix.button import MDIconButton
from kivy.config import Config
from kivy.factory import Factory
from kivy.uix.popup import Popup
from lub import *

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "700")

Window.clearcolor = (.80, .242, .126, 1)


class App(MDApp):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.setView(self)
        self.number_record_per_page = 5
        self.number_record = 0
        self.number_page = 1
        self.current_page = 1
        self.buffer = None
        self.set_noun = ['И.п.', 'ед.ч.']
        self.set_adj = ['И.п.', 'м.р.', 'ед.ч.']
        self.set_verb = ['пр.вр.', '1.л.', 'м.р.', 'ед.ч.']

    def build(self):
        root = Builder.load_file('lib.kv')
        return root

    def count_number_page(self):
        self.number_page = self.number_record // self.number_record_per_page
        if self.number_record % self.number_record_per_page > 0:
            self.number_page += 1

    def to_first_page(self, current_page):
        self.current_page = 1
        current_page.text = str(self.current_page)
        self.show_data('nan')

    def to_last_page(self, current_page):
        dctnry = self.controller.get_data()
        self.current_page = len(dctnry) // self.number_record_per_page + 1
        current_page.text = str(self.current_page)
        self.show_data('nan')

    def to_x_page(self, current_page, sign):
        dctnry = self.controller.get_data()
        if sign == '+':
            if (len(dctnry) // self.number_record_per_page) >= self.current_page:
                self.current_page += 1
                current_page.text = str(self.current_page)
        elif sign == '-':
            if self.current_page - 1 > 0:
                self.current_page -= 1
                current_page.text = str(self.current_page)
        self.show_data('nan')

    def show_data(self, filter):
        if type(filter) != str:
            filter = filter.text
        self.clear_label()

        x = self.root.ids.dictionary_screen.ids.gl_2
        y = self.root.ids.dictionary_screen.ids.gl_3

        n = (self.current_page - 1) * self.number_record_per_page
        if filter == 'nan':
            dctnry = self.controller.get_data()
        elif filter == '':
            dctnry = self.controller.get_data()
        else:
            dctnry = self.controller.search_data(filter)
        for j in range(self.number_record_per_page):

            if len(dctnry) <= j:
                for k in range(1):
                    x.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))
                    y.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))
            elif n + j >= len(dctnry):
                for k in range(1):
                    x.add_widget(Label(text='', color=(1, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))
                    y.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))

            else:
                x.add_widget(
                    Label(text=str(dctnry[j + n]), color=(0, .26, .41, 1), halign='center', valign='center',
                          text_size=(150, 700 / self.number_record_per_page)))
                y.add_widget(
                    MDIconButton(id=str(dctnry[j + n]), icon="magnify", on_press=self.view_forms,
                                 icon_color=(.14, .26, 1, 1), halign='center',
                                 valign='center', size_hint=(1.5, 1.0)))
                y.add_widget(
                    MDIconButton(id=str(dctnry[j + n]), icon="delete", on_press=self.controller.del_word,
                                 icon_color=(.14, .26, .41, 1), halign='center', valign='center',
                                 size_hint=(1.5, 1.0)))

        self.root.ids.dictionary_screen.ids.number_record.text = "Кол-во записей: " + str(len(dctnry))
        self.number_record = len(dctnry)
        self.root.ids.dictionary_screen.ids.last_page.text = str(
            len(dctnry) // self.number_record_per_page + 1)

    def view_forms(self, word):
        self.root.current = 'Формы'
        self.show_data_form(str(word.id))
        self.WindowManager.current = self.root.ids.ref_screen



    def clear_label(self):
        x = self.root.ids.dictionary_screen.ids.gl_2
        y = self.root.ids.dictionary_screen.ids.gl_3
        y.clear_widgets()
        x.clear_widgets()

    def to_x_record(self, num):
        self.clear_label()
        self.number_record_per_page = num
        self.count_number_page()
        self.show_data('nan')




    def to_first_page_form(self, current_page):
        self.current_page = 1
        current_page.text = str(self.current_page)
        self.show_data_form(self.word)

    def to_last_page_form(self, current_page):
        dctnry = self.controller.get_forms(self.word)
        self.current_page = len(dctnry) // self.number_record_per_page + 1
        current_page.text = str(self.current_page)
        self.show_data_form(self.word)

    def to_x_page_form(self, current_page, sign):
        dctnry = self.controller.get_forms(self.word)
        if sign == '+':
            if (len(dctnry) // self.number_record_per_page) >= self.current_page:
                self.current_page += 1
                current_page.text = str(self.current_page)
        elif sign == '-':
            if self.current_page - 1 > 0:
                self.current_page -= 1
                current_page.text = str(self.current_page)
        self.show_data_form(self.word)

    def show_data_form(self, word):
        self.word = word
        self.clear_label_forms()
        z = self.root.ids.forms_screen.ids.box
        x = self.root.ids.forms_screen.ids.gl_form_2
        y = self.root.ids.forms_screen.ids.gl_form_3

        n = (self.current_page - 1) * self.number_record_per_page

        dict_osn = self.controller.get_form_n(self.word)
        for i in range(3):
            z.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                           text_size=(150, 700 / self.number_record_per_page)))
        for i in range(3):
            z.add_widget(
                Label(text=str(dict_osn[i]), color=(0, .26, .41, 1), halign='center', valign='center',
                      text_size=(150, 700 / self.number_record_per_page)))

        dctnry = self.controller.get_forms(self.word)
        for j in range(self.number_record_per_page):
            if len(dctnry) <= j:
                for k in range(2):
                    x.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))
                    y.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))
            elif n + j >= len(dctnry):
                for k in range(2):
                    x.add_widget(Label(text='', color=(1, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))
                    y.add_widget(Label(text='', color=(0, .26, .41, 1), halign='center', valign='center',
                                       text_size=(150, 700 / self.number_record_per_page)))

            else:
                x.add_widget(
                    Label(text=str(dctnry[j + n][0]), color=(0, .26, .41, 1), halign='center', valign='center',
                          text_size=(150, 700 / self.number_record_per_page)))
                x.add_widget(
                    Label(text=str(dctnry[j + n][1]), color=(0, .26, .41, 1), halign='center', valign='center',
                          text_size=(150, 700 / self.number_record_per_page)))
                y.add_widget(
                    MDIconButton(id=str(dctnry[j + n]), icon="auto-fix", on_press=self.edit_forms,
                                 icon_color=(.14, .26, 1, 1), halign='center',
                                 valign='center', size_hint=(1.5, 1.0)))


        self.root.ids.forms_screen.ids.number_record.text = "Кол-во записей: " + str(len(dctnry))
        self.number_record = len(dctnry)
        self.root.ids.forms_screen.ids.last_page.text = str(
            len(dctnry) // self.number_record_per_page + 1)


    def clear_label_forms(self):
        z = self.root.ids.forms_screen.ids.box
        x = self.root.ids.forms_screen.ids.gl_form_2
        y = self.root.ids.forms_screen.ids.gl_form_3
        z.clear_widgets()
        y.clear_widgets()
        x.clear_widgets()

    def to_x_record_form(self, num):
        self.clear_label_forms()
        self.number_record_per_page = num
        self.count_number_page()
        self.show_data_form(self.word)

    def edit_forms(self, form):
        self.form = str(form.id)
        Factory.EditPopup().open(form.id)

    def set_case_noun(self, case):
        self.set_noun[0] = str(case)

    def set_count_noun(self, count):
        self.set_noun[1] = str(count)

    def set_case_adj(self, case):
        self.set_adj[0] = str(case)

    def set_sex_adj(self, sex):
        self.set_adj[1] = str(sex)

    def set_count_adj(self, count):
        self.set_adj[2] = str(count)

    def set_time_verb(self, time):
        self.set_verb[0] = str(time)

    def set_face_verb(self, face):
        self.set_verb[1] = str(face)

    def set_sex_verb(self, sex):
        self.set_verb[2] = str(sex)

    def set_count_verb(self, count):
        self.set_verb[3] = str(count)




    class MenuScreen(Screen):
        pass

    class DictionaryScreen(Screen):
        pass

    class RefScreen(Screen):
        pass

    class FormsScreen(Screen):
        pass

    class GenScreen(Screen):
        pass

    class WindowManager(ScreenManager):
        pass
