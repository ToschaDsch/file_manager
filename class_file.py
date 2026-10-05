from dataclasses import dataclass
from pathlib import Path

from variables import MyColor


@dataclass
class StatusFile:
    unchecked: str = 'neu'
    by_checking: str = 'am Prüfung'
    checked: str = 'geprüft'
    to_send: str = 'zu schicken'
    is_send: str = 'verschickt'
    dict_of_status = {unchecked: 0, by_checking: 1, checked: 2, to_send: 3, is_send: 4}
    list_of_status = [unchecked, by_checking, checked, to_send, is_send]
    dict_of_palette_colors = {unchecked: 'rgb' + str(MyColor.unchecked),
                              by_checking: 'rgb' + str(MyColor.by_checking),
                              checked: 'rgb' + str(MyColor.checked),
                              to_send: 'rgb' + str(MyColor.to_send),
                              is_send: 'rgb' + str(MyColor.is_send)}


class ClassFile:
    def __init__(self, name: str, path: Path, status: str = StatusFile.unchecked, nr_protokol: int = 0,
                 subdir: str = ''):
        self.name: str = name
        self.path: Path = path
        self.status: str = status
        self.nr_protokol = nr_protokol
        self.subdir: str = subdir
        self.name_of_file_in_the_table = ''
        self.name_of_the_plan = ''
        self.index = ''

    def __str__(self):
        return self.name

    @property
    def print_values(self):
        return f"{self.name_of_file_in_the_table} {self.index} \t {self.name_of_the_plan}"
