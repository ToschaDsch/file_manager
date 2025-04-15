import os
import sys

from PySide6 import QtWidgets, QtGui

from variables import VariablesForMenus
from window_1 import GeneralWindow


def load_general_menu():
    basedir = os.path.dirname(__file__)
    #basedir = os.path.join(basedir, 'icons\\icon.png')  # icon for general program

    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon(basedir))
    screen = app.primaryScreen()
    size = screen.size()
    VariablesForMenus.screen_width = size.width()
    VariablesForMenus.screen_height = size.height()
    VariablesForMenus.general_window = GeneralWindow()
    VariablesForMenus.general_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    load_general_menu()
