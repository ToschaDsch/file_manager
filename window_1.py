import json
import os

from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QComboBox, QTableWidgetItem, \
    QPushButton, QLabel, QCheckBox
from sortedcontainers import SortedDict
import variables
from class_file import StatusFile, ClassFile
from functions_without_general_class import open_the_file, check_the_file, get_dict_of_checked_files, \
    get_dict_of_by_checking_files, get_dict_to_send_files, get_list_of_send_files, get_only_folders, \
    move_from_by_checking_to_checked, move_from_checked_to_to_send, move_from_unchecked_to_by_checking, \
    get_list_of_all_protocols, get_list_of_file_in_the_protocol, move_the_file_to_new_protocol, get_only_files, \
    start_the_file, make_a_buton_with_a_picture, new_list_to_the_combobox
from variables import VariablesForMenus


class GeneralWindow(QMainWindow):
    def __init__(self, show_static: bool = False, *args):
        super(GeneralWindow, self).__init__()
        pixmap = QtGui.QPixmap(variables.icon)
        app_icon = QtGui.QIcon(pixmap)
        self.setWindowIcon(app_icon)

        self.setWindowTitle(variables.name_of_the_program)

        general_layout = QVBoxLayout()

        # variables
        dir_0 = variables.dir_for_checking
        raw_list_of_all_folder = os.listdir(dir_0)
        self._list_of_years = list(filter(lambda x: (x[:4] == variables.name_of_the_folder), raw_list_of_all_folder))
        self._current_year: str = variables.current_year
        self._current_dir_year = variables.dir_for_checking + '\\' + variables.current_year
        self._current_list_of_files_for_the_year = []
        self._current_project = variables.current_project
        self._current_dir_project = ''
        self._current_list_of_files = []
        self._current_dir_incoming_docs = ''
        self._list_of_all_files_of_the_project = []
        self._list_class_files = []
        self._dict_by_checking_files = dict()
        self._dict_checked_files = dict()
        self._dict_to_send_files = dict()
        self._set_send_files = {}
        self._selected_rows: list[int] = list()
        self._unchecked_files = 0

        self._picked_files = []
        self._current_aim_to_move = StatusFile.list_of_status[0]
        self._list_of_protocols: list[str] = []
        self._current_protocol = ''
        self._list_send_protocols = []
        self._number_of_current_protocol = 0
        self._last_two_numbers_of_current_protocol = '00'

        self._show_static = show_static
        if show_static:
            self._folder_that_i_dont_need = variables.folder_that_i_dont_need
        else:
            self._folder_that_i_dont_need = variables.folder_that_i_dont_need + variables.folder_that_i_dont_need_with_statik

        # menu up
        self.combobox_aim_to_move = QComboBox()
        self.combobox_protocol = QComboBox()

        self.combobox_dir_year = QComboBox()
        self.combobox_dir_project = QComboBox()
        self.general_table = QTableWidget()
        list_of_files = self._list_of_years
        self.make_top_menu(layout=general_layout, list_of_dir=list_of_files)

        # menu up 2 (my projects)
        self.combobox_my_projects = QComboBox()
        self.button_delete_the_project = QPushButton()
        self.button_add_the_project = QPushButton()
        self._dict_of_my_projects: SortedDict = SortedDict({"-":{'year': None,
                                                                                        'status': None}})
        self._dict_of_my_projects.update(variables.my_projects) # name, year, status of files

        self.make_top_menu_2(layout=general_layout,
                             dict_of_my_projects=self._dict_of_my_projects)

        # middle menu
        self.make_menu_middle(layout=general_layout)

        # menus at the bottom
        self.button_to_move = QPushButton(VariablesForMenus.text_for_button_move_file)
        self.button_to_open = QPushButton(VariablesForMenus.text_for_button_open)
        self.button_to_open_list_of_protocols = QPushButton(VariablesForMenus.open_list_of_files_in_the_protocol)
        self.button_move_the_file_to_the_protocol = QPushButton(VariablesForMenus.text_move_the_file)
        self.combobox_aim_to_move = QComboBox()
        self.combobox_protocol = QComboBox()
        self.make_menu_bottom(layout=general_layout)

        self.combobox_dir_year.setCurrentText(variables.current_year)
        self.refresh_all()
        self.combobox_dir_project.setCurrentText(variables.current_project)
        self.combobox_my_projects.setCurrentIndex(0)

        widget = QWidget()
        widget.setLayout(general_layout)
        self.setCentralWidget(widget)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                self.on_application_activated()
        super().changeEvent(event)

    def on_application_activated(self):
        # This function runs automatically when the app is focused
        self.select_rows(row_indices=self._selected_rows)

    def closeEvent(self, event):
        # save the settings by file close
        path = variables.file_of_settings
        settings_0 = {'dir_for_checking': variables.dir_for_checking,
                      'year': variables.current_year,
                      'project': self._current_project,
                      'show_static': self._show_static,
                      'my_projects': self._dict_of_my_projects}
        try:
            with open(path, 'w') as file:
                json.dump(settings_0, file, indent=4)
            print(f"Dictionary saved as JSON to '{path}'.")
        except Exception as e:
            print(f"Error saving file: {e}")
        event.accept()  # Accept the close event

    def make_menu_bottom(self, layout: QVBoxLayout):
        self.make_menu_bottom_0(layout=layout)  # files open, copy
        self.make_menu_bottom_1(layout=layout)  # protocols
        self.make_menu_bottom_2(layout=layout)  # settings (show static)
        self.make_menu_bottom_3(layout=layout)  # color palette

    def make_menu_bottom_0(self, layout: QVBoxLayout):
        """menu with buttons open, copy"""
        layout_bottom = QHBoxLayout()

        self.button_to_open.setEnabled(False)
        self.button_to_open.clicked.connect(self.open_the_picked_files)
        layout_bottom.addWidget(self.button_to_open)

        separator = QLabel('  ')
        separator.setFixedWidth(VariablesForMenus.separator_for_menu_bottom)
        #layout_bottom.addWidget(separator)

        self.button_to_move.setEnabled(False)
        self.button_to_move.clicked.connect(self.move_the_picked_files)
        layout_bottom.addWidget(self.button_to_move)

        # aim to move
        for dir_i in variables.list_of_aims:
            self.combobox_aim_to_move.addItem(str(dir_i))
        current_index = 0
        self.combobox_aim_to_move.setCurrentIndex(current_index)
        self.combobox_aim_to_move.currentIndexChanged.connect(self.change_index_of_combobox_aim)

        layout_bottom.addWidget(self.combobox_aim_to_move)

        layout.addLayout(layout_bottom)

    def make_menu_bottom_1(self, layout: QVBoxLayout):
        """menu with buttons protocols"""
        layout_bottom = QHBoxLayout()

        self.make_list_of_protocols()
        layout_bottom.addWidget(self.combobox_protocol)

        button_open_the_protocol = QPushButton(VariablesForMenus.open_the_protocol)
        button_open_the_protocol.clicked.connect(self.open_the_protokol)
        layout_bottom.addWidget(button_open_the_protocol)

        self.button_move_the_file_to_the_protocol.clicked.connect(self.move_the_file_to_the_protocol)
        layout_bottom.addWidget(self.button_move_the_file_to_the_protocol)
        self.button_move_the_file_to_the_protocol.setEnabled(False)

        layout_bottom.addWidget(self.button_to_open_list_of_protocols)
        self.button_to_open_list_of_protocols.clicked.connect(self.show_the_files_in_the_protocol)

        layout.addLayout(layout_bottom)

    def open_the_protokol(self):
        """the function opens the current protocol"""
        all_files = get_only_files(path=self._current_dir_project)
        variants_of_the_name: list[str] = []
        for variant in variables.names_of_protocol:
            variants_of_the_name.append(self._current_protocol.replace(variables.protocol, variant))
        for name in variants_of_the_name.copy():
            variants_of_the_name.append(self._current_project[:7] + " " + name)
        for name_i in variants_of_the_name:
            for type_of_the_file in variables.types_of_the_protocol_files:
                name_of_the_file = name_i + type_of_the_file
                if name_of_the_file in all_files:
                    file_path = self._current_dir_project + "\\" + name_of_the_file
                    print(file_path)
                    start_the_file(path=file_path)
                    return None
        return None

    def move_the_file_to_the_protocol(self):
        current_protocol = int(self._last_two_numbers_of_current_protocol)
        for file in self._picked_files:
            if file.nr_protokol != current_protocol and file.status != StatusFile.unchecked:
                protocol = variables.protocol + ' ' + str(int(self._last_two_numbers_of_current_protocol))
                move_the_file_to_new_protocol(file=file, new_protocol=protocol)
                file.nr_protokol = current_protocol
        self.update_the_table()
        self.select_rows(row_indices=self._selected_rows)

    def make_menu_bottom_2(self, layout: QVBoxLayout):
        """menu with settings (show static)"""
        layout_bottom = QHBoxLayout()

        checkbox_show_static = QCheckBox(VariablesForMenus.text_show_static)
        checkbox_show_static.setChecked(self._show_static)
        checkbox_show_static.stateChanged.connect(self.checkbox_changed_show_static)
        layout_bottom.addWidget(checkbox_show_static)

        layout.addLayout(layout_bottom)

    def checkbox_changed_show_static(self, state: int):
        self._show_static = bool(state)
        if state:
            self._folder_that_i_dont_need = variables.folder_that_i_dont_need
        else:
            self._folder_that_i_dont_need = variables.folder_that_i_dont_need + variables.folder_that_i_dont_need_with_statik
        self.refresh_all()
        current_project = self._current_project
        self.new_list_to_the_combobox_my_projects(dict_of_my_projects=self._dict_of_my_projects,
                                                  current_project=self._current_project)
        self.make_the_project_active(project=current_project)

    def show_the_files_in_the_protocol(self):
        self.make_list_of_file_in_the_protocol()

    @staticmethod
    def make_menu_bottom_3(layout: QVBoxLayout):
        """menu for color palette at the bottom"""
        layout_palette = QHBoxLayout()
        for name_of_label, color in StatusFile.dict_of_palette_colors.items():
            label_i = QLabel(name_of_label + ' ->')
            label_i.setAlignment(Qt.AlignmentFlag.AlignCenter)
            color_i = f"background-color:{color}"
            label_i.setFixedHeight(20)
            label_i.setStyleSheet(color_i)
            layout_palette.addWidget(label_i)

        layout.addLayout(layout_palette)

    def open_the_picked_files(self):
        for file in self._picked_files:
            open_the_file(file=file)
        self.select_rows(row_indices=self._selected_rows)

    def make_list_of_file_in_the_protocol(self):
        list_of_file_in_protocol = get_list_of_file_in_the_protocol(list_of_all_files=self._list_class_files,
                                                                    current_dir_incoming_docs=self._current_dir_incoming_docs,
                                                                    number_of_current_protocol=int(
                                                                        self._last_two_numbers_of_current_protocol)
                                                                    )
        if list_of_file_in_protocol is None:
            return None
        print('list of files for ', self._current_protocol)
        for file in list_of_file_in_protocol:
            print(file.print_values)
        return None

    def make_list_of_protocols(self):
        self.combobox_protocol.clear()
        self._list_of_protocols, self._list_send_protocols = get_list_of_all_protocols(
            dir_protocols=self._current_dir_project)
        model = self.combobox_protocol.model()
        n = 0
        for i, protocol_i in enumerate(self._list_of_protocols):
            self.combobox_protocol.addItem(str(protocol_i))
            model.setData(model.index(i, 0), QColor(*variables.MyColor.checked),
                          QtCore.Qt.ItemDataRole.BackgroundRole)
            n = i

        for i, protocol_i in enumerate(self._list_send_protocols):
            self.combobox_protocol.addItem(str(protocol_i))
            model.setData(model.index(n + i + 1, 0), QColor(*variables.MyColor.is_send),
                          QtCore.Qt.ItemDataRole.BackgroundRole)

        current_index = 0
        self.combobox_protocol.currentIndexChanged.connect(self.change_index_of_combobox_protocol)
        self.combobox_protocol.setCurrentIndex(current_index)
        self.change_index_of_combobox_protocol(current_index)

    def move_the_picked_files(self):
        for file_i in self._picked_files:
            self.move_the_file(file=file_i)
        self.update_the_table()
        self.select_rows(row_indices=self._selected_rows)

    def move_the_file(self, file: ClassFile):
        # check - can I move it
        if not self.check_can_i_move_it(status=file.status):
            return None
        # V:\P-2024\P24-117_BPD Neub. 4 Wohngeb. BA1 Ehrenkirchen-Kirchhofen\Eingang Prüfunterlagen\Pläne Haus
        # 1\P24-117_BEW_H1-BU104_-_BA1_UG_UP20602.pdf if self._number_of_current_protocol
        if int(self._last_two_numbers_of_current_protocol) == 0:
            protocol = ''
        else:
            protocol = variables.protocol + ' ' + str(int(self._last_two_numbers_of_current_protocol))
        # copy the file to the aim
        match self._current_aim_to_move:
            case StatusFile.by_checking:
                move_from_unchecked_to_by_checking(file=file, protocol=protocol)
            case StatusFile.checked:
                if file.status == StatusFile.unchecked:
                    move_from_unchecked_to_by_checking(file=file, protocol=protocol)
                    self.move_the_file(file=file)
                else:
                    move_from_by_checking_to_checked(file=file, protocol=protocol)
            case _:
                if file.status == StatusFile.unchecked:
                    move_from_unchecked_to_by_checking(file=file, protocol=protocol)
                    self.move_the_file(file=file)
                elif file.status == StatusFile.by_checking:
                    move_from_by_checking_to_checked(file=file, protocol=protocol)
                    self.move_the_file(file=file)
                else:
                    move_from_checked_to_to_send(file=file, protocol=protocol)
        file.nr_protokol = int(self._last_two_numbers_of_current_protocol)
        return None

    def check_can_i_move_it(self, status: str) -> bool:
        """the function checks - can you move the file,
        unchecked -> by checking -> checked -> to send -> send
        you can move only in direction ->"""
        if status not in StatusFile.dict_of_status:
            print('There is not status - ', status)
            return False
        nr_status = StatusFile.dict_of_status[status]
        if self._current_aim_to_move not in StatusFile.dict_of_status:
            print('There is not aim - ', self._current_aim_to_move)
            return False
        nr_aim = StatusFile.dict_of_status[self._current_aim_to_move]
        return nr_status < nr_aim

    def make_menu_middle(self, layout: QVBoxLayout):
        # make the table
        header = ('name', 'status', 'Nr. Prüfbericht', 'directory')
        b = VariablesForMenus.b
        h = VariablesForMenus.h
        self.general_table.setFixedWidth(b)
        self.general_table.setFixedHeight(h)
        self.general_table.setColumnCount(len(header))
        self.general_table.setHorizontalHeaderLabels(header)
        self.general_table.setColumnWidth(0, int(VariablesForMenus.column_0_name))
        self.general_table.setColumnWidth(1, int(VariablesForMenus.column_1_status))
        self.general_table.setColumnWidth(2, int(VariablesForMenus.column_2_protokol))
        self.general_table.setColumnWidth(3, int(VariablesForMenus.column_3_subdir))
        self.general_table.itemSelectionChanged.connect(self.table_selection_changed)
        self.general_table.itemDoubleClicked.connect(self.double_click_the_table_item)
        layout.addWidget(self.general_table)

        try:
            index = self._current_list_of_files_for_the_year.index(variables.current_project)
        except ValueError:
            print('There is no file for this year - ', variables.current_project)
            index = 0
        self.combobox_dir_project.setCurrentIndex(index)

    def open_the_directory(self):
        start_the_file(path=self._current_dir_project)

    def make_top_menu(self, layout: QVBoxLayout, list_of_dir):
        # make the current directory
        layout_directory = QHBoxLayout()
        layout_directory.addWidget(self.combobox_dir_year)
        layout_directory.addWidget(self.combobox_dir_project)

        #button open the folder
        button_open = QPushButton()
        path = variables.path_buttons_open_the_folder
        h = variables.VariablesForMenus.height_buttons
        b = VariablesForMenus.width_buttons
        make_a_buton_with_a_picture(path_for_the_pis=path, h=h, b=b,
                                    button=button_open,
                                    function=self.open_the_directory)
        layout_directory.addWidget(button_open)
        layout.addLayout(layout_directory)

        # make it for year
        for dir_i in list_of_dir:
            self.combobox_dir_year.addItem(str(dir_i))
        if variables.current_year not in list_of_dir:
            current_index = 0
        else:
            current_index = list_of_dir.index(variables.current_year)
        self.combobox_dir_year.setCurrentIndex(current_index)
        self.combobox_dir_year.currentIndexChanged.connect(self.change_index_of_combobox_year)

        self._current_list_of_files_for_the_year = get_only_folders(path=self._current_dir_year)
        self._current_project = variables.current_project
        self._current_dir_project = self._current_dir_year + '\\' + self._current_project
        self._list_of_all_files_of_the_project = get_only_folders(path=self._current_dir_project)
        self._current_dir_incoming_docs = self._current_dir_project + '\\' + variables.incoming_docs

        # make it for the project
        for dir_i in self._current_list_of_files_for_the_year:
            self.combobox_dir_project.addItem(str(dir_i))
        self.combobox_dir_project.currentIndexChanged.connect(self.change_index_of_combobox_project)

    def make_top_menu_2(self, layout: QVBoxLayout, dict_of_my_projects: SortedDict):
        # make the menu for my projects
        layout_my_projects = QHBoxLayout()
        layout_my_projects.addWidget(QLabel(VariablesForMenus.my_projects))
        # buttons
        layout_my_projects.addWidget(self.button_add_the_project)
        layout_my_projects.addWidget(self.button_delete_the_project)
        path = variables.path_buttons_my_projects_plus
        h = variables.VariablesForMenus.height_buttons
        b = VariablesForMenus.width_buttons
        make_a_buton_with_a_picture(path_for_the_pis=path, h=h, b=b,
                                    button=self.button_add_the_project,
                                    function=self.add_the_project_to_my_project)
        path = variables.path_buttons_my_projects_delete
        make_a_buton_with_a_picture(path_for_the_pis=path, h=h, b=b,
                                    button=self.button_delete_the_project,
                                    function=self.delete_the_project_from_my_project)
        # combobox
        layout_my_projects.addWidget(self.combobox_my_projects)
        self.new_list_to_the_combobox_my_projects(dict_of_my_projects=dict_of_my_projects,
                                                    current_project=self._current_project)
        self.combobox_my_projects.currentIndexChanged.connect(self.change_index_of_combobox_my_projects)

        layout.addLayout(layout_my_projects)


    def change_index_of_combobox_my_projects(self, index: int):
        current_project = list(self._dict_of_my_projects)[index]
        if current_project in ("", '-', None):
            return
        self.make_the_project_active(project=current_project)


    def make_the_project_active(self, project: str) -> int:
        if project not in self._dict_of_my_projects:
            return 0
        self._current_year = self._dict_of_my_projects[project]['year']
        self.combobox_dir_year.setCurrentText(self._current_year)
        self.refresh_all()
        self._current_project = project
        self.combobox_dir_project.setCurrentText(self._current_project)
        return self._unchecked_files

    def add_the_project_to_my_project(self):
        self._dict_of_my_projects[self._current_project] = {'year': self._current_year,
                                                            'status': None}
        self.new_list_to_the_combobox_my_projects(dict_of_my_projects=self._dict_of_my_projects,
                                                    current_project=self._current_project)

    def new_list_to_the_combobox_my_projects(self, dict_of_my_projects: SortedDict,
                                 current_project: str) -> None:
        self.combobox_my_projects.clear()
        model = self.combobox_my_projects.model()
        i = 0
        for key, value in  dict_of_my_projects.items():
            if key == "-":
                self.combobox_my_projects.addItem(key)
                i+=1
                continue
            status = self.check_status_of_the_project(project=key)
            value['status'] = status
            string = key + '    |   ' + status if status else key
            self.combobox_my_projects.addItem(string)
            if status:
                model.setData(model.index(i, 0), QColor(*variables.MyColor.unchecked),
                                  QtCore.Qt.ItemDataRole.BackgroundRole)
            i+=1
        self.combobox_my_projects.setCurrentText(current_project)

    def check_status_of_the_project(self, project: str) -> str|None:
        if self.make_the_project_active(project=project):
            return variables.new_plans
        else:
            return None

    def delete_the_project_from_my_project(self):
        current_project = self.combobox_my_projects.currentText()
        if current_project == "-":
            return None
        if current_project in self._dict_of_my_projects:
            del self._dict_of_my_projects[current_project]
        new_list_to_the_combobox(combobox=self.combobox_my_projects,
                                 dict_of_my_projects=self._dict_of_my_projects,
                                 current_project=self._current_project)
        return None

    def table_selection_changed(self):
        if VariablesForMenus.table_insert:
            return None
        items = self.general_table.selectedItems()
        rows = [x.row() for x in items]
        self._selected_rows = rows
        self._picked_files = [self._list_class_files[x] for x in rows]
        list_of_button = [self.button_to_open,
                          self.button_to_move,
                          self.button_move_the_file_to_the_protocol]
        if len(self._picked_files) > 0:
            is_enabled = True
        else:
            is_enabled = False
        for button in list_of_button:
            button.setEnabled(is_enabled)
        self.aim_to_change()
        return None

    def select_rows(self, row_indices: list[int]):
        VariablesForMenus.table_insert = True
        for row in row_indices:
            for col in range(self.general_table.columnCount()):
                item = self.general_table.item(row, col)
                if item:  # Make sure the cell is not None
                    item.setSelected(True)
        VariablesForMenus.table_insert = False

    def aim_to_change(self):
        """if you select the files, you need to know status for all the files
        status - status min"""
        # find minimal status
        set_of_status = {x.status for x in self._picked_files}
        status = StatusFile.unchecked
        if StatusFile.is_send in set_of_status:
            status = StatusFile.is_send
        if StatusFile.to_send in set_of_status:
            status = StatusFile.to_send
        if StatusFile.checked in set_of_status:
            status = StatusFile.checked
        if StatusFile.by_checking in set_of_status:
            status = StatusFile.by_checking
        if StatusFile.unchecked in set_of_status:
            status = StatusFile.unchecked
        # find new aim
        index = 3
        match status:
            case StatusFile.unchecked:
                index = 1
            case StatusFile.by_checking:
                index = 2
        self._current_aim_to_move = StatusFile.list_of_status[index]
        self.combobox_aim_to_move.setCurrentIndex(index - 1)

    def add_an_element_in_the_table(self, row_number: int, new_element: ClassFile):
        self.general_table.insertRow(row_number)
        VariablesForMenus.table_insert = True
        # b0
        self.general_table.setItem(row_number, 0, QTableWidgetItem(str(new_element.name[:-4])))
        item_status = QLabel(new_element.status)
        item_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color = StatusFile.dict_of_palette_colors[new_element.status]
        color_i = f"background-color:{color}"
        item_status.setStyleSheet(color_i)
        self.general_table.setCellWidget(row_number, 1, item_status)
        protocol_widget = QTableWidgetItem(str(new_element.nr_protokol))
        protocol_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.general_table.setItem(row_number, 2, protocol_widget)
        self.general_table.setItem(row_number, 3, QTableWidgetItem(new_element.subdir))
        VariablesForMenus.table_insert = False

    def change_index_of_combobox_aim(self, index: int):
        self._current_aim_to_move = StatusFile.list_of_status[index + 1]

    def change_index_of_combobox_protocol(self, index: int):
        """the function checks if the protocol is not send"""
        self._number_of_current_protocol = index
        if index >= len(self._list_of_protocols):
            self.combobox_protocol.setCurrentIndex(0)
            return None
        name_of_current_protocol = self._list_of_protocols[index]
        self._current_protocol = name_of_current_protocol
        if name_of_current_protocol not in self._list_of_protocols:
            return None
        for i in range(4, len(name_of_current_protocol)):
            if name_of_current_protocol[i].isnumeric() and name_of_current_protocol[i + 1].isnumeric():
                number = name_of_current_protocol[i: i + 2]
                self._last_two_numbers_of_current_protocol = number
                break
        return None

    def change_index_of_combobox_year(self, index: int):
        self._current_year = self._list_of_years[index]
        self._current_dir_year = variables.dir_for_checking + '\\' + self._current_year
        variables.current_year = self._current_year
        self._current_list_of_files_for_the_year = get_only_folders(path=self._current_dir_year)
        self._current_project = self._current_list_of_files_for_the_year[0]
        self._current_dir_project = self._current_dir_year + '\\' + self._current_project
        self.combobox_dir_project.clear()
        for dir_i in self._current_list_of_files_for_the_year:
            self.combobox_dir_project.addItem(str(dir_i))

        current_index = 0
        self.combobox_dir_project.setCurrentIndex(current_index)

        self.make_list_of_protocols()

    def change_index_of_combobox_project(self, index: int):
        self._current_project = self._current_list_of_files_for_the_year[index]
        self.refresh_all()

    def refresh_all(self):
        self._current_dir_project = self._current_dir_year + '\\' + self._current_project
        self._list_of_all_files_of_the_project = get_only_folders(path=self._current_dir_project)

        self.make_list_for_all_files()
        self.make_list_of_protocols()
        self.update_the_table()


    def update_the_table(self):
        """dell all elements of the table and make it again"""
        self.general_table.setRowCount(0)
        for i, element_i in enumerate(self._list_class_files):
            self.add_an_element_in_the_table(row_number=i, new_element=element_i)

    def make_list_for_all_files(self):
        """the function looks for all files in variables.incoming_docs
        and in folders
        then the function makes lists or dicts of the files in oder folders with status (unchecked, checked at cet.)"""
        if variables.incoming_docs not in self._list_of_all_files_of_the_project:
            print('there is no', variables.incoming_docs)
            return None
        self._current_dir_incoming_docs = self._current_dir_project + '\\' + variables.incoming_docs
        list_of_folders = get_only_folders(path=self._current_dir_incoming_docs)
        set_of_folders = set(list_of_folders) - set(self._folder_that_i_dont_need)
        list_of_folders = list(set_of_folders)
        self._current_list_of_files = []
        # files in folders
        for folder_i in list_of_folders:
            dir_i = self._current_dir_incoming_docs + '\\' + folder_i
            for file in os.listdir(dir_i):
                for end_of_the_file  in variables.types_of_the_draw_files:
                    if file.endswith(end_of_the_file):
                        self._current_list_of_files.append([os.path.join(file), os.path.join(dir_i, file), folder_i])
        # files without folders
        dir_i = self._current_dir_incoming_docs
        for file in os.listdir(dir_i):
            for end_of_the_file  in variables.types_of_the_draw_files:
                if file.endswith(end_of_the_file):
                    self._current_list_of_files.append([os.path.join(file), os.path.join(dir_i, file), ''])
        # list of all send files
        self._dict_by_checking_files = get_dict_of_by_checking_files(path=self._current_dir_project)
        self._dict_checked_files = get_dict_of_checked_files(path=self._current_dir_project,
                                                             dict_by_checking=self._dict_by_checking_files)
        self._dict_to_send_files = get_dict_to_send_files(path=self._current_dir_project,
                                                          dict_checked_files=self._dict_checked_files)
        self._set_send_files = set(get_list_of_send_files(path=self._current_dir_project))
        self._list_class_files = self.make_list_of_class_files(self._current_list_of_files)
        return None

    def make_list_of_class_files(self, list_of_file_path) -> list[ClassFile]:
        """the function makes two lists of files other files and send files"""
        list_of_classes_first = []
        list_of_classes_second = []  # send
        self._unchecked_files = 0
        for name, path, folder in list_of_file_path:
            new_class = self.make_class_for_a_file(name, path, folder)
            if new_class.status == StatusFile.is_send:
                list_of_classes_second.append(new_class)
            else:
                list_of_classes_first.append(new_class)
                if new_class.status == StatusFile.unchecked:
                    self._unchecked_files += 1

        return list_of_classes_first + list_of_classes_second

    def make_class_for_a_file(self, name: str, path: str, folder: str) -> ClassFile:
        status = StatusFile.unchecked
        protocol_nr = 0
        # by checking
        result = check_the_file(name=name, folder=folder, status_name=StatusFile.by_checking,
                                dict_i=self._dict_by_checking_files)
        if result:
            status = result[0]
            protocol_nr = result[1]

        # checked file
        result = check_the_file(name=name, folder=folder, status_name=StatusFile.checked,
                                dict_i=self._dict_checked_files)
        if result:
            status = result[0]
            protocol_nr = result[1]
        # to send file
        result = check_the_file(name=name, folder=folder, status_name=StatusFile.to_send,
                                dict_i=self._dict_to_send_files)
        if result:
            status = result[0]
            protocol_nr = result[1]
        # send file
        if name[:-4] in self._set_send_files:
            status = StatusFile.is_send
        return ClassFile(name=name, path=path, subdir=folder, status=status, nr_protokol=protocol_nr)

    def double_click_the_table_item(self, item: QTableWidgetItem):
        file: ClassFile = self._list_class_files[item.row()]
        open_the_file(file=file)
