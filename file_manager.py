import json
import os
import sys

from PySide6 import QtWidgets, QtGui

import variables
from functions_without_general_class import get_only_folders
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


def get_dict_settings_from_file() -> dict:
    path = variables.file_of_settings
    if os.path.exists(path):
        try:
            # Open and read the file
            with open(path, 'r') as file:
                content = file.read()

            # Try to parse the content as JSON
            try:
                data_dict = json.loads(content)
                print("JSON data successfully parsed as dictionary:")
                print(data_dict)
                return {'dir_for_checking': data_dict['dir_for_checking'],
                        'year': data_dict['year'],
                        'project': data_dict['project'],
                        'show_static': data_dict['show_static']}
            except json.JSONDecodeError:
                print("The file content is not valid JSON.")
        except Exception as e:
            print(f"Error reading the file: {e}")
    else:
        print(f"The file does not exist at: {path}")
        dir_0 = variables.dir_for_checking
        raw_list_of_all_folder = os.listdir(dir_0)
        list_of_years = list(filter(lambda x: (x[:4] == variables.name_of_the_folder), raw_list_of_all_folder))
        current_year = list_of_years[-1]
        current_list_of_files_for_the_year = get_only_folders(path=dir_0 + '\\' + current_year)
        project = current_list_of_files_for_the_year[0]
        settings_0 = {'dir_for_checking': variables.dir_for_checking,
                      'year': current_year,
                      'project': project,
                      'show_static': False}
        try:
            with open(path, 'w') as file:
                json.dump(settings_0, file, indent=4)
            print(f"Dictionary saved as JSON to '{path}'.")
        except Exception as e:
            print(f"Failed to save JSON: {e}")
        return settings_0


if __name__ == "__main__":
    # update settings
    settings = get_dict_settings_from_file()
    variables.dir_for_checking = settings['dir_for_checking']
    variables.current_year = settings['year']
    variables.current_project = settings['project']
    show_static = settings['show_static']
    load_general_menu(show_static=show_static)
