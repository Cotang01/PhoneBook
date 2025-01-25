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
    def load_book(self):
        self.repo.load_contacts()

    @log_exec_and_catch_excep
    def save_book(self):
        self.repo.save_contacts()

    def get_work_time(self):
        """ Returns working time in seconds. """
        return time() - self.launched_at

    @log_exec_and_catch_excep
    def add_contact(self, data: dict[str, str]):
        self.repo.add_contact(Contact(**data))

    @log_exec_and_catch_excep
    def remove_contact(self, contact_id) -> bool:
        return self.repo.delete_contact_by_id(contact_id=contact_id)

    @log_exec_and_catch_excep
    def modify_contact(self, contact_id, data) -> bool:
        contact = self.repo.get_contact_by_id(contact_id)
        if contact is None:
            return False
        for field, val in data.items():
            if val:
                contact.__dict__[field] = val
        return True

    @log_exec_and_catch_excep
    def get_str_contacts(self) -> Dict[int, Contact]:
        return self.repo.get_contacts()

    def __str__(self):
        return f'{self.__class__.__name__}, working for {self.get_work_time()}'
