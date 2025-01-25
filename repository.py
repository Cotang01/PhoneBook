from model import Contact

from typing import Dict


class PhoneBookRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.contacts: dict[int, Contact] = {}
        self.sep = ';'
        self.work_ready = False

    @staticmethod
    def work_ready_checker(func):
        def wrapper(self, *args, **kwargs):
            if self.work_ready is not True:
                self.load_contacts()
            return func(self, *args, **kwargs)
        return wrapper

    def load_contacts(self) -> None:
        with open(file=self.file_path, mode='r', encoding='UTF-8') as f:
            for i, line in enumerate(f.readlines(), start=1):
                name, num, info = line.split(self.sep)
                self.contacts[i] = Contact(name, num, info.strip())
        self.work_ready = True

    @work_ready_checker
    def save_contacts(self) -> None:
        with open(file=self.file_path, mode='w+', encoding='UTF-8') as f:
            for c in self.contacts.values():
                f.write(f'{self.sep.join(c.__dict__.values())}\n')
        self.contacts = {}
        self.work_ready = False

    @work_ready_checker
    def get_contact_by_id(self, contact_id: int) -> Contact:
        if not isinstance(contact := self.contacts.get(contact_id), Contact):
            raise KeyError(f'No contact with such id: {contact_id}.')
        return contact

    @work_ready_checker
    def delete_contact_by_id(self, contact_id: int) -> bool:
        try:
            self.contacts.pop(contact_id)
            return True
        except KeyError:
            raise

    @work_ready_checker
    def get_contacts(self) -> Dict[int, Contact]:
        return self.contacts

    @work_ready_checker
    def add_contact(self, contact) -> None:
        self.contacts[len(self.contacts)+1] = contact

    def __str__(self):
        return f'{'\n'.join(map(str, self.contacts.values()))}'
