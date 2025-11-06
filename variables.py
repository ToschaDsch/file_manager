from dataclasses import dataclass

from PySide6.QtWidgets import QMainWindow

name_of_the_program: str = 'file_manager_'
file_of_settings: str = 'settings.txt'
current_year: str = 'P-2024'
current_project: str = 'P24-117_BPD Neub. 4 Wohngeb. BA1 Ehrenkirchen-Kirchhofen'
my_projects: dict = dict()

types_of_the_draw_files = (".pdf", ".PDF")
types_of_the_protocol_files = ('.doc', '.docx')
dir_for_checking: str = 'V:\\'
name_of_the_folder: str = 'P-20'

# pictures for the buttons
path_buttons_my_projects_plus: str = 'pictures//plus.png'
path_buttons_my_projects_delete: str = 'pictures//trash.png'
path_buttons_open_the_folder: str = 'pictures//open.png'
icon: str = './pictures/icon_ferminium.jpg'

# types files to check
incoming_docs: str = 'Eingang Prüfunterlagen'
checked_files: str = 'geprüfte Unterlagen'
by_checking: str = '0_Pläne zu prüfen'
checked_files_planes: str = '1_geprüfte Pläne'
files_to_send: str = '2_Pläne zu schicken'

file_name_not_to_scan: set[str] = {by_checking, checked_files_planes, files_to_send,
                         'ELBA-Schritte', 'Pläne neue Indexe','Pläne alte Indexe', 'ELBA-Schritte'}
folder_that_i_dont_need: list[str] = ['überholt', 'Überholt', 'überholte Pläne']   #
folder_that_i_dont_need_with_statik: list[str] = ['Statik', 'statik']
variants_of_the_ending: set[str] = {'_PE-PoP', '_PE-PoPG', '_PE-PmP', '_PE-PmPG', '_PE-F', '_PE-U', '_PE-G', ''}
names_of_protocol: set[str] = {'Prüfbericht_', 'Prüfbericht ', 'Pruefbericht_', 'Pruefbericht ', 'Prüfbericht', 'Pruefbericht'}
protocol: str = 'Prüfbericht'
list_of_aims: list[str] = [by_checking, checked_files_planes, files_to_send]
text_of_the_excel_file: str = 'Verlauf'
text_index: str = ' Index '
name_of_the_useful_cell_in_the_excel_file: str = "Inhalt"
new_plans = "neue Pläne!"


@dataclass
class VariablesForMenus:
    # size of the general windows
    b: int = 700
    h: int = 600

    table_insert = False

    screen_width: int = 100
    screen_height: int = 100
    general_window: QMainWindow = None
    # width to general table
    column_0_name: int = 350
    column_1_status: int = 100
    column_2_protokol: int = 100
    column_3_subdir: int = 100
    # menu at the bottom
    separator_for_menu_bottom: int = 10
    text_for_button_move_file: str = 'den Plan kopieren nach ->'
    text_for_button_open: str = 'die Pläne öffnen'
    open_list_of_files_in_the_protocol: str = 'Liste der Pläne im Prüfbericht'
    open_the_protocol: str = "öffnen den Prüfbericht"
    text_show_static: str = "zeige Statik"
    text_move_the_file: str = 'Verschieben die Pläne zum Prüfbericht'
    # menu my projects
    my_projects: str = "Meine Projekte"
    height_buttons: int = 20
    width_buttons: int = 40


@dataclass
class MyColor:
    unchecked: tuple[int] = (250, 100, 100)
    by_checking: tuple[int] = (150, 100, 100)
    checked: tuple[int] = (150, 150, 100)
    to_send: tuple[int] = (100, 150, 100)
    is_send: tuple[int] = (100, 100, 150)
