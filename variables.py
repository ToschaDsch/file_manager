from dataclasses import dataclass

dir_for_checking = 'V:'
name_of_the_folder = 'P-20'
incoming_docs = 'Eingang Prüfunterlagen'
by_checking = '0_Pläne zu prüfen'
checked_files = 'geprüfte Unterlagen'
checked_files_planes = '1_geprüfte Pläne'
files_to_send = '2_Pläne zu schicken'
folder_that_i_dont_need = ['Statik', 'statik', 'überholt', 'Überholt', 'überholte Pläne']
variants_of_the_ending = {'PE-PoP', 'PE-PoPG', 'PE-PmP', 'PE-PmPG', 'PE-F', 'PE-U', 'PE-G'}
names_of_protocol = {'Prüfbericht_', 'Prüfbericht ', 'Pruefbericht_', 'Pruefbericht ', 'Prüfbericht', 'Pruefbericht'}
protocol = 'Prüfbericht'
list_of_aims = [by_checking, checked_files_planes, files_to_send]


@dataclass
class VariablesForMenus:
    # size of the general windows
    b = 700
    h = 600

    table_insert = False

    screen_width = 100
    screen_height = 100
    general_window = None
    # width to general table
    column_0_name = 350
    column_1_status = 100
    column_2_protokol = 100
    column_3_subdir = 100
    # menu at the bottom
    separator_for_menu_bottom = 30
    text_for_button_move_file = 'den Plan schieben nach ->'
    text_for_button_open = 'die Pläne offnen'


@dataclass
class MyColor:
    unchecked = (250, 100, 100)
    by_checking = (150, 100, 100)
    checked = (150, 150, 100)
    to_send = (100, 150, 100)
    is_send = (100, 100, 150)
