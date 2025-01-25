from model import Contact
from repository import PhoneBookRepository

from logging import getLogger, Logger, basicConfig, INFO
from typing import Dict
from time import time
from functools import wraps


class PhoneBookController:
    """ App's controller layer class """
    def __init__(self, repo: PhoneBookRepository, logger: Logger = None):
        self.repo = repo
        match logger.__class__.__name__:
            case 'Logger':
                self.logger = logger
            case _:
                self.logger = getLogger(__name__)
                basicConfig(filename='default.log', filemode='w', level=INFO)
        self.launched_at = time()

    @staticmethod
    def log_exec_and_catch_excep(func):
        """ Decorator that logs execution of functions and catches
        exceptions. """
        @wraps(func)  # to access __name__
        def wrapper(self, *args, **kwargs):
            self.logger.info(f'Executing {func.__name__} with'
                             f'(args: {args}, kwargs: {kwargs})')
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                self.logger.error(f'{e.__class__.__name__} has occurred: {e}')
                return False
        return wrapper

    @log_exec_and_catch_excep
    def load_book(self) -> None:
        """ Makes call to repository layer to load Contacts' data. """
        self.repo.load_contacts()

    @log_exec_and_catch_excep
    def save_book(self) -> None:
        """ Makes call to repository layer to save current state of
         Contacts' data. """
        self.repo.save_contacts()

    def get_work_time(self) -> float:
        """ Returns working time in seconds. """
        return time() - self.launched_at

    @log_exec_and_catch_excep
    def add_contact(self, data: dict[str, str]) -> None:
        """ Creates new Contact obj and calls repository layer to add obj. """
        self.repo.add_contact(Contact(**data))

    @log_exec_and_catch_excep
    def remove_contact(self, contact_id: int) -> bool:
        """ Calls repository layer to remove Contact obj by contact_id. """
        return self.repo.delete_contact_by_id(contact_id=contact_id)

    @log_exec_and_catch_excep
    def modify_contact(self, contact_id: int, data: Dict[str, str]) -> bool:
        """ Calls repository layer to replace Contact obj data with new one
         if not blank. For example if name: '', then name doesn't change. """
        contact = self.repo.get_contact_by_id(contact_id)
        if contact is None:
            return False
        for field, val in data.items():
            if val:
                contact.__dict__[field] = val
        return True

    @log_exec_and_catch_excep
    def get_str_contacts(self) -> Dict[int, Contact]:
        """ Calls repository layer to get all Contacts. """
        return self.repo.get_contacts()

    def __str__(self):
        return f'{self.__class__.__name__}, working for {self.get_work_time()}'
