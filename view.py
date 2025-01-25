from controller import PhoneBookController
from typing import Dict

from parsers import IniLocalizationParser


class PhoneBookView:
    def __init__(self, controller: PhoneBookController, valid_langs: dict):
        self.cont = controller
        self.valid_langs = valid_langs
        self.text_lines = self.set_localization()

    @staticmethod
    def print_prettied_output(func):
        """ Decorator that prints view functions results with borders.
         Function must return str obj for decorator to print it. """

        def wrapper(self, *args, **kwargs):
            res = []
            cur_max = 0
            func_res = func(self, *args, **kwargs)
            text_split = func_res.split('\n')
            for r in text_split:
                cur_max = max(cur_max, len(r))
            cur_max += 2
            res.append(f'╔{'═' * cur_max}╗')
            for r in text_split:
                res.append(f'║ {r} {'║'.rjust(cur_max - len(r) - 1)}')
            res.append(f'╚{'═' * cur_max}╝')
            print('\n'.join(res))
            return func_res

        return wrapper

    def get_user_choice(self) -> str:
        """ Gets and validates user's input to be in range of valid options of
        PhoneBook functionality. """
        choice = input(self.text_lines['get_user_option'])
        if not choice.isdigit() or not 0 < (choice := int(choice)) < 10:
            print('⌀')
            choice = self.get_user_choice()
        return choice

    def set_localization(self) -> Dict[str, str]:
        """ Takes user's localization choice and loads strings from
         .ini file with localization data (key = value)"""
        lang_choice = self._get_localization_choice()
        return IniLocalizationParser.read_properties_file(
            self.valid_langs[lang_choice])

    def _get_localization_choice(self) -> str:
        """ Gets user's input and checks if input is in keys of
         provided cfg.ini file {lang: path_to_strings.ini, ...}"""
        choice = input('Choose language/Выберите язык:\n[ru, eng] 🖝 ')
        # choice = 'ru'
        if choice.lower() not in self.valid_langs.keys():
            print('⌀')
            choice = self._get_localization_choice()
        return choice

    @print_prettied_output
    def show_contacts(self) -> str:
        """ Returns current state of Contacts. """
        contacts_data = '\n'.join(
            [f'{k} - {v}' for k, v in self.cont.get_str_contacts().items()]
        )
        return f'{self.text_lines['contacts_header']}\n{contacts_data}'

    @print_prettied_output
    def get_menu(self) -> str:
        """ Returns valid options of PhoneBook functionality. """
        return self.text_lines['menu_options']

    @print_prettied_output
    def load_book(self) -> str:
        """ Makes call to controller layer to load data. """
        self.cont.load_book()
        return self.text_lines['book_loaded']

    @print_prettied_output
    def modify_contact(self) -> str:
        """ Makes call to controller layer to modify one of Contact's data
         by id. """
        contact_id = self._get_id_of_contact()
        data = self._get_data_for_update()
        if self.cont.modify_contact(contact_id, data):
            return self.text_lines['modify_cont_success']
        return (f"{self.text_lines['modify_cont_fail_no_such_id']} "
                f"{contact_id}")

    def _get_data_for_update(self) -> Dict[str, str]:
        """ Asks user which data to change: \n
        name -> input(); number -> input(); info -> input(). """
        res = {'name': self.text_lines['modify_contact_name'],
               'number': self.text_lines['modify_contact_number'],
               'info': self.text_lines['modify_contact_info']}
        for field, req in res.items():
            res[field] = input(req)
        return res

    @print_prettied_output
    def save_book(self) -> str:
        """ Makes call to controller layer to save current state of data
        into file and returns respective answer. """
        self.cont.save_book()
        return self.text_lines['book_saved']

    @print_prettied_output
    def create_new_contact(self) -> str:
        """ Gets data from user's input and makes call to controller layer to
         create new Contact obj based on retrieved data. """
        data = self._get_new_contact_data()
        self.cont.add_contact(data=data)
        return self.text_lines['contact_created']

    def _get_new_contact_data(self) -> Dict[str, str]:
        """ Gets new 1.name, 2.number and 3.info from input() calls and
         returns them as dict. """
        data = {'name': '', 'number': '', 'info': ''}
        input_requests = [
            self.text_lines['new_contact_name'],
            self.text_lines['new_contact_number'],
            self.text_lines['new_contact_info'],
        ]
        for field, req in zip(data.keys(), input_requests):
            data[field] = input(req)
        return data

    def _get_id_of_contact(self) -> int:
        """ Gets input() until it's number and returns it. """
        id_to_delete = input(self.text_lines['id_to_change'])
        if not id_to_delete.isdigit():
            id_to_delete = self._get_id_of_contact()
        return int(id_to_delete)

    @print_prettied_output
    def remove_contact(self) -> str:
        """ Makes call to controller layer to delete contact by id from
        input(). Returns respective answer."""
        choice = self._get_id_of_contact()
        if self.cont.remove_contact(contact_id=choice):
            return self.text_lines['contact_remove_success']
        return self.text_lines['contact_remove_fail']

    @print_prettied_output
    def change_lang(self) -> str:
        """ Replaces current localization lines with new ones. Returns
        respective answer."""
        self.text_lines = self.set_localization()
        return self.text_lines['lang_change_success']

    @print_prettied_output
    def show_working_time(self) -> str:
        """ Returns working time of controller as 'x.xx seconds' """
        return (f'{round(self.cont.get_work_time(), ndigits=2)} '
                f'{self.text_lines['work_time']}')

    def __str__(self):
        return f'{self.text_lines}'
