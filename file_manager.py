import os
import sys

from PySide6 import QtWidgets, QtGui

import functions_without_general_class
import variables
from variables import VariablesForMenus
from window_1 import GeneralWindow


def load_general_menu(show_static: bool = False):
    basedir = os.path.dirname(__file__)
    # basedir = os.path.join(basedir, 'icons\\icon.png')  # icon for general program
    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon(basedir))
    screen = app.primaryScreen()
    size = screen.size()
    VariablesForMenus.screen_width = size.width()
    VariablesForMenus.screen_height = size.height()
    VariablesForMenus.general_window = GeneralWindow(show_static=show_static)
    VariablesForMenus.general_window.show()
    sys.exit(app.exec())


def get_dict_settings_from_file() -> dict | None:
    path = variables.file_of_settings
    if os.path.exists(path):
        return functions_without_general_class.read_the_setting_from_the_file(path=path)
    else:
        return functions_without_general_class.make_default_settings(path=path)

def set_the_settings() -> bool:
    settings = get_dict_settings_from_file()
    variables.dir_for_checking = settings['dir_for_checking']
    variables.current_year = settings['year']
    variables.current_project = settings['project']
    show_me_static = settings['show_static']
    return show_me_static

if __name__ == "__main__":
    # update settings
    show_me_static = set_the_settings()
    load_general_menu(show_static=show_me_static)
