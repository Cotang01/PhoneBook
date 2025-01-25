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
        self.view = PhoneBookView(
            PhoneBookController(
                PhoneBookRepository(
                    file_path=contacts_path
                ),
                self.logger
            ),
            self.cfg.lang
        )

    def run(self):
        """ Main app function managing it's following behaviour based on
        user's choices. """
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
                    self.view.change_lang()
                case 8:
                    self.view.show_working_time()
                case 9:
                    break
