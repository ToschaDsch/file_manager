from dataclasses import dataclass
from variables import MyColor


@dataclass
class StatusFile:
    unchecked = 'neu'
    by_checking = 'am Prüfung'
    checked = 'geprüft'
    to_send = 'zu schicken'
    is_send = 'verschickt'
    dict_of_status = {unchecked: 0, by_checking: 1, checked: 2, to_send: 3, is_send: 4}
    list_of_status = [unchecked, by_checking, checked, to_send, is_send]
    dict_of_palette_colors = {unchecked: 'rgb' + str(MyColor.unchecked),
                              by_checking: 'rgb' + str(MyColor.by_checking),
                              checked: 'rgb' + str(MyColor.checked),
                              to_send: 'rgb' + str(MyColor.to_send),
                              is_send: 'rgb' + str(MyColor.is_send)}


class ClassFile:
    def __init__(self, name: str, path: str, status: str = StatusFile.unchecked, nr_protokol: int = 0,
                 subdir: str = ''):
        self.name = name
        self.path = path
        self.status = status
        self.nr_protokol = nr_protokol
        self.subdir = subdir
        self.name_of_file_in_the_table = ''
        self.name_of_the_plan = ''
        self.index = ''

    def __str__(self):
        return self.name

    @property
    def print_values(self):
        return f"{self.name_of_file_in_the_table} {self.index} \t {self.name_of_the_plan}"
