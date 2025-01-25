

class Contact:
    """ Model that represents phone book contacts data. """
    def __init__(self, name: str, number: str, info: str):
        __slots__ = ['name', 'number', 'info']
        self.name = name
        self.number = number
        self.info = info

    def __str__(self):
        return f'{self.name} | {self.number} | {self.info}'
