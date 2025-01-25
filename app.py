from typing import Dict
from controller import PhoneBookController
from repository import PhoneBookRepository
from view import PhoneBookView
from parsers import IniConfigParse, IniLocalizationParser
from logger import get_logger


class PhoneBookApp:
    """
    Class managing user commands.
    """
    def __init__(self, contacts_path: str):
        self.cfg = IniConfigParse()
        self.logger = get_logger(
            self.cfg.log_config['level'],
            self.cfg.log_config['format'],
            self.cfg.log_config['filename'],
        )
        self.valid_langs = self.cfg.lang
        self.repo = PhoneBookRepository(file_path=contacts_path)
        self.cont = PhoneBookController(self.repo, self.logger)
        self.view = PhoneBookView(self.cont, self.set_localization())

    def set_localization(self) -> Dict:
        """ Takes user's localization choice and loads strings from
         .ini file with localization data (key = value)"""
        lang_choice = self._get_localization_choice()
        return IniLocalizationParser.read_properties_file(
            self.valid_langs[lang_choice])

    def _get_localization_choice(self):
        """ Gets user's input and checks if input is in keys of
         provided cfg.ini file {lang: path_to_strings.ini, ...}"""
        choice = input('Choose language/Выберите язык:\n[ru, eng] 🖝 ')
        # choice = 'ru'
        if choice.lower() not in self.valid_langs.keys():
            print('⌀')
            choice = self._get_localization_choice()
        return choice

    def run(self):
        """ Main app function managing it's following behaviour. """
        while True:
            self.view.get_menu()
            choice = self.view.get_user_choice()
            match choice:
                case 1:
                    self.view.load_book()
                case 2:
                    self.view.show_contacts()
                case 3:
                    self.view.create_new_contact()
                case 4:
                    self.view.show_contacts()
                    self.view.remove_contact()
                case 5:
                    self.view.modify_contact()
                case 6:
                    self.view.save_book()
                case 7:
                    self.view.change_lang(self.set_localization())
                case 8:
                    self.view.show_working_time()
                case 9:
                    break
