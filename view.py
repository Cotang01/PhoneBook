from controller import PhoneBookController
from typing import Dict, Iterable, Callable, Generator


class PhoneBookView:
    def __init__(self, controller: PhoneBookController,
                 text_lines: Dict[str, str]):
        self.cont = controller
        self.text_lines = text_lines

    @staticmethod
    def print_prettied_output(func):
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

    def get_user_choice(self):
        choice = input(self.text_lines['get_user_option'])
        if not choice.isdigit() or not 0 < (choice := int(choice)) < 10:
            print('⌀')
            choice = self.get_user_choice()
        return choice

    @print_prettied_output
    def show_contacts(self):
        contacts_data = '\n'.join(
            [f'{k} - {v}' for k, v in self.cont.get_str_contacts().items()]
        )
        return f'{self.text_lines['contacts_header']}\n{contacts_data}'

    @print_prettied_output
    def get_menu(self) -> str:
        return self.text_lines['menu_options']

    @print_prettied_output
    def load_book(self):
        self.cont.load_book()
        return self.text_lines['book_loaded']

    @print_prettied_output
    def modify_contact(self):
        contact_id = self._get_id_of_contact()
        data = self._get_data_for_update()
        try:
            self.cont.modify_contact(contact_id, data)
            return self.text_lines['modify_cont_success']
        except KeyError:
            return (f"{self.text_lines['modify_cont_fail_no_such_id']} "
                    f"{contact_id}")

    def _get_data_for_update(self):
        res = {'name': self.text_lines['modify_contact_name'],
               'number': self.text_lines['modify_contact_number'],
               'info': self.text_lines['modify_contact_info']}
        for field, req in res.items():
            res[field] = input(req)
        return res

    @print_prettied_output
    def save_book(self):
        self.cont.save_book()
        return self.text_lines['book_saved']

    @print_prettied_output
    def create_new_contact(self):
        data = self._get_new_contact_data()
        self.cont.add_contact(data=data)
        return self.text_lines['contact_created']

    def _get_new_contact_data(self):
        data = {'name': '', 'number': '', 'info': ''}
        input_requests = [
            self.text_lines['new_contact_name'],
            self.text_lines['new_contact_number'],
            self.text_lines['new_contact_info'],
        ]
        for field, req in zip(data.keys(), input_requests):
            data[field] = self._get_input_data(req)
        return data

    def _get_id_of_contact(self) -> int:
        id_to_delete = input(self.text_lines['id_to_change'])
        if not id_to_delete.isdigit():
            id_to_delete = self._get_id_of_contact()
        return int(id_to_delete)

    @print_prettied_output
    def remove_contact(self):
        choice = self._get_id_of_contact()
        if self.cont.remove_contact(contact_id=choice):
            return self.text_lines['contact_remove_success']
        return self.text_lines['contact_remove_fail']

    @staticmethod
    def _get_input_data(req: str):
        return input(req)

    @print_prettied_output
    def change_lang(self, new_text_lines: Dict[str, str]):
        self.text_lines = new_text_lines
        return self.text_lines['lang_change_success']

    @print_prettied_output
    def show_working_time(self):
        return (f'{round(self.cont.get_work_time(), ndigits=2)} '
                f'{self.text_lines['work_time']}')

    def __str__(self):
        return f'{self.text_lines}'
