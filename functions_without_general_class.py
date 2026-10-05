import io
import os
import shutil
from enum import Enum
from pathlib import Path
from typing import Any
import json
import openpyxl
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QPushButton, QComboBox

import variables
from class_file import StatusFile, ClassFile


class Settings(Enum):
    dir_for_checking = 'dir_for_checking'
    dir_for_save = 'dir_for_save'
    name_of_the_folder = 'name_of_the_folder'
    year = 'year'
    project = 'project'
    show_static = 'show_static'
    my_projects = 'my_projects'


def new_list_to_the_combobox(combobox: QComboBox, dict_of_my_projects: dict,
                             current_project: Path) -> None:
    combobox.clear()
    for key, value in dict_of_my_projects.items():
        combobox.addItem(key)
    combobox.setCurrentText(current_project.name)

def make_a_buton_with_a_picture(path_for_the_pis: str, h: int, b: int,
                                button: QPushButton, function):
    pixmap = QPixmap(path_for_the_pis)
    if pixmap.isNull():
        print("no picture", path_for_the_pis)

    new_size = QSize(h, h)
    scaled = pixmap.scaled(new_size,
                           Qt.AspectRatioMode.KeepAspectRatio,
                           Qt.TransformationMode.SmoothTransformation)
    button.setIcon(scaled)
    button.setIconSize(new_size)
    button.setFixedWidth(b)
    button.clicked.connect(function)

def get_list_of_all_protocols(dir_protocols: Path) -> tuple[list[str], list[str]]:
    filter_files = {
        file.stem
        for file in get_only_files(dir_protocols)
        if file.suffix in variables.types_of_the_protocol_files
    }

    filter_files_2: set[str] = set()

    for variant in variables.names_of_protocol:
        for file_name in filter_files:
            if variant in file_name:
                n = file_name.index(variant)
                filter_files_2.add(file_name[n + len(variant):])

    send_protocols: list[str] = []
    not_send_protocols: list[str] = []

    for protocol in filter_files_2:
        if protocol.isnumeric():
            send_protocols.append(f"{variables.protocol}_{protocol}")
        else:
            not_send_protocols.append(f"{variables.protocol}{protocol}")

    if not not_send_protocols:
        not_send_protocols = [f"{variables.protocol}_00"]

    return not_send_protocols, send_protocols


def start_file_is_send(path: Path, name: Path, subdir: Path,
) -> None:
    base_dir = path.parent  # remove file name

    if subdir:
        base_dir = base_dir.parent  # remove subdir

    checked_dir = (
        Path(variables.checked_files)
        / base_dir.relative_to(variables.incoming_docs)
    )

    for ending in variables.variants_of_the_ending:
        candidate = checked_dir / (
            f"{name.stem}{ending}{name.suffix}"
        )

        if candidate.is_file():
            start_the_file(candidate)
            return


def check_the_file(name: Path, dict_i: dict, folder: Path, status_name: str) -> tuple[str, int] | bool:
    for protocol_nr_i, dict_of_files_i in dict_i.items():
        if folder == '':
            if protocol_nr_i == 0:
                if name in dict_i[protocol_nr_i]:
                    return status_name, protocol_nr_i
            else:
                if name in dict_i[protocol_nr_i][0]:
                    return status_name, protocol_nr_i
            continue
        else:
            if isinstance(dict_of_files_i, list):
                continue
            for folder_j, list_of_files_j in dict_of_files_i.items():
                if folder_j == folder:
                    if name in list_of_files_j:
                        return status_name, protocol_nr_i
    return False


def get_dict_to_send_files(path: Path, dict_checked_files: dict[str, Path]) -> dict:
    path2 = variables.files_to_send
    return get_dict_of(path=path, dict_checked_files=dict_checked_files, path2=path2)

def get_dict_of_checked_files(path: Path, dict_by_checking: dict) -> dict:
    path2 = variables.checked_files_planes
    return get_dict_of(path=path, dict_checked_files=dict_by_checking, path2=path2)

def get_dict_of(path: Path, dict_checked_files: dict, path2: Path,
) -> dict:
    checked_path = path / variables.checked_files

    if not dict_checked_files:
        return {}

    if not (checked_path / variables.files_to_send).is_dir():
        print("no subdir", variables.files_to_send)
        return {}

    target_path = checked_path / path2
    all_folders = get_only_folders(target_path)

    return get_dict_with_protocol_files(
        path=target_path,
        folders=all_folders,
    )


def get_dict_of_by_checking_files(path: Path) -> dict:
    checked_path = path / variables.checked_files

    if not checked_path.is_dir():
        print("no subdir !!", variables.checked_files)
        return {}

    checking_path = checked_path / variables.by_checking

    if not checking_path.is_dir():
        print("no subdir", variables.by_checking)
        return {}

    return get_dict_with_protocol_files(
        path=checking_path,
        folders=get_only_folders(checking_path),
    )


def get_dict_with_protocol_files(
    path: Path,
    folders: list[Path],
) -> dict:
    dict_protokol_files = {}

    for folder_path in folders:
        folder_name = folder_path.name

        for protocol_name in variables.names_of_protocol:
            if protocol_name not in folder_name:
                continue

            nummer_str = folder_name.replace(protocol_name, "")

            try:
                nummer = int(nummer_str)
            except Exception as err:
                print("there is no number", folder_name)
                print(f"Unexpected {err=}, {type(err)=}")
                return {}

            dict_protokol_files[nummer] = {
                0: get_only_files(folder_path)
            }

            for subfolder in get_only_folders(folder_path):
                dict_protokol_files[nummer][subfolder.name] = (
                    get_only_files(subfolder)
                )

            break

    return dict_protokol_files

def get_list_of_send_files(path: Path) -> list[str]:
    checked_path = path / variables.checked_files

    if not checked_path.is_dir():
        print("no subdir", variables.checked_files)
        return []

    pdf_names: set[str] = {p.name for p in checked_path.iterdir() if p.is_file()}

    ignored = set(variables.file_name_not_to_scan)

    for folder in checked_path.iterdir():
        if not folder.is_dir() or folder.name in ignored:
            continue

        pdf_names |= {p.name for p in folder.iterdir() if p.is_file()}

    result: list[str] = []

    for filename in pdf_names:
        if not filename.endswith(".pdf"):
            continue

        stem = Path(filename).stem

        for n in (8, 7, 5):
            if stem[-n:] in variables.variants_of_the_ending:
                result.append(stem[:-n])
                break
        else:
            result.append(stem)

    return result


def get_only_folders(path: Path) -> list[Path]:
    try:
        return [item for item in path.iterdir() if item.is_dir()]
    except Exception as err:
        print("error, by get_the_folders", err)
        return []


def get_only_files(path: Path) -> list[Path]:
    try:
        return [item for item in path.iterdir() if item.is_file()]
    except Exception as err:
        print("error, by get_only_files", err)
        return []


from pathlib import Path


def start_file_by_status(path: Path, name: Path, protokol_nr: int, folder_to_check: Path, subdir: Path,
) -> None:
    relative = path.relative_to(variables.incoming_docs)
    path = Path(variables.checked_files) / folder_to_check / relative.parent

    if subdir:
        path = path.parent

    for protocol_prefix in variables.names_of_protocol:
        protocol_name = f"{protocol_prefix}{protokol_nr}"
        file_path = path / protocol_name

        if subdir:
            file_path /= subdir

        file_path /= name

        if file_path.is_file():
            start_the_file(file_path)
            return


def start_the_file(path: Path) -> None:
    try:
        os.startfile(path)  # or os.startfile(str(path))
    except Exception as err:
        print("startfile error", path)
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def copy_the_file(old_path: Path, new_path: Path) -> None:
    print("I copy the file", old_path.name)

    if not print_the_information(old_path, new_path):
        return

    try:
        shutil.copyfile(old_path, new_path)
    except Exception as err:
        print("copy error", old_path.name)
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def print_the_information(old_path: Path, new_path: Path, name: Path=None) -> bool:
    print("from", old_path)
    print("to", new_path)
    print("---->>>>>")

    if not old_path.is_file():
        print("there is no file", old_path.name)
        return False

    new_path.parent.mkdir(parents=True, exist_ok=True)

    return True



def move_the_file(old_path: Path, new_path: Path, name: Path=None) -> None:
    print("I move the file", old_path.name)

    if not print_the_information(
        old_path=old_path,
        new_path=new_path,
    ):
        return

    try:
        shutil.move(old_path, new_path)
    except Exception as err:
        print("move error", old_path.name)
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def move_from_unchecked_to_by_checking(file: ClassFile, protocol: str = ''):
    relative_path = file.path.relative_to(Path(variables.incoming_docs))

    new_path = (Path(variables.checked_files)/ variables.by_checking/ protocol/ relative_path)

    file.status = StatusFile.by_checking

    copy_the_file(old_path=file.path,new_path=new_path)


def move_from_by_checking_to_checked(file: ClassFile, protocol: str = ''):
    relative_path = file.path.relative_to(Path(variables.incoming_docs))

    source_root = (Path(variables.checked_files)/ variables.by_checking)

    target_root = (Path(variables.checked_files)/ variables.checked_files_planes)

    if protocol:
        source_root /= protocol
        target_root /= protocol

    old_path = source_root / relative_path
    new_path = target_root / relative_path

    copy_the_file(
        old_path=old_path,
        new_path=new_path,
    )

    file.status = StatusFile.checked


def move_from_checked_to_to_send(
    file: ClassFile,
    protocol: str = "",
) -> None:
    relative_path = file.path.relative_to(variables.incoming_docs)

    checked_root = (Path(variables.checked_files)/ variables.checked_files_planes)

    send_root = (Path(variables.checked_files)/ variables.files_to_send)

    if protocol:
        checked_root /= protocol
        send_root /= protocol

    old_path = checked_root / relative_path
    new_path = send_root / relative_path

    copy_the_file(old_path=old_path, new_path=new_path)

    file.status = StatusFile.to_send


def move_the_file_to_new_protocol(file: ClassFile, new_protocol: str):
    list_of_status = []
    match file.status:
        case StatusFile.by_checking:
            list_of_status = [StatusFile.by_checking]
        case StatusFile.checked:
            list_of_status = [StatusFile.by_checking, StatusFile.checked]
        case StatusFile.to_send | StatusFile.is_send:
            list_of_status = [StatusFile.by_checking, StatusFile.checked, StatusFile.to_send]
    for status in list_of_status:
        move_the_file_to_new_protocol_with_status(file=file, new_protocol=new_protocol,
                                                  status=status)


def move_the_file_to_new_protocol_with_status(file: ClassFile, new_protocol: str, status: str):
    old_protocol = variables.protocol + ' ' + str(file.nr_protokol)
    status_path = variables.by_checking
    match status:
        case StatusFile.by_checking:
            status_path = variables.by_checking
        case StatusFile.checked:
            status_path = variables.checked_files_planes
        case StatusFile.to_send:
            status_path = variables.files_to_send
    move_the_file_with_the_status(file=file, new_protocol=new_protocol, old_protocol=old_protocol,
                                  status_path=status_path)


def move_the_file_with_the_status(file: ClassFile, new_protocol: str, status_path: Path, old_protocol: str):
    relative_path = file.path.relative_to(
        Path(variables.incoming_docs)
    )

    base_path = Path(variables.checked_files) / status_path

    old_path = base_path / old_protocol / relative_path
    new_path = base_path / new_protocol / relative_path

    move_the_file(old_path=old_path,new_path=new_path)


def open_the_file(file: ClassFile):
    match file.status:
        case StatusFile.unchecked:
            start_the_file(path=file.path)
        case StatusFile.by_checking:
            start_file_by_status(path=file.path, name=file.name, protokol_nr=file.nr_protokol,
                                 folder_to_check=variables.by_checking, subdir=file.subdir)
        case StatusFile.checked:
            start_file_by_status(path=file.path, name=file.name, protokol_nr=file.nr_protokol,
                                 folder_to_check=variables.checked_files_planes, subdir=file.subdir)
        case StatusFile.to_send:
            start_file_by_status(path=file.path, name=file.name, protokol_nr=file.nr_protokol,
                                 folder_to_check=variables.files_to_send, subdir=file.subdir)
        case StatusFile.is_send:
            start_file_is_send(path=file.path, name=file.name, subdir=file.subdir)


def get_list_of_file_in_the_protocol(list_of_all_files: list[ClassFile], number_of_current_protocol: int,
                                     current_dir_incoming_docs: Path) -> list[ClassFile] | None:

    list_of_file_in_protocol = [
        file
        for file in list_of_all_files
        if file.nr_protokol == number_of_current_protocol
    ]

    all_excel_files = [
        file
        for file in get_only_files(current_dir_incoming_docs)
        if file.suffix == ".xlsx"
    ]

    excel_file: Path | None = None

    for file in all_excel_files:
        if variables.text_of_the_excel_file in file.name:
            excel_file = file
            break

    if excel_file is None:
        return None

    dict_files = file_excel_open_get_date(file_name=excel_file)

    if dict_files is None:
        return None

    return get_new_list_of_files_in_the_protocol(
        dict_files=dict_files,
        list_of_files=list_of_file_in_protocol,
    )


def get_new_list_of_files_in_the_protocol(dict_files: dict, list_of_files: list[ClassFile]) -> list[ClassFile]:
    new_list_of_file = []
    dict_of_names = dict()
    for file_table in dict_files:
        if len(file_table) < 2:
            continue
        try:
            index = file_table.index(variables.text_index)
            file_name = file_table[:index].replace(" ", "")
            index = file_table[index + 7:].replace(" ", "")
            if index == '-':
                index = ''
        except ValueError:
            file_name = file_table
            index = ''
        value = dict_files[file_table]
        if file_name in dict_of_names:  # check the new index
            if index > dict_of_names[file_name][1]:
                dict_of_names[file_name] = [index, value]
            else:
                continue
        else:  # there is no file in the dict
            dict_of_names[file_name] = [index, value]
    for file in list_of_files:
        for file_name, values in dict_of_names.items():
            index, value = values

            if file.name.name.find(file_name) > 0:
                file_2 = ClassFile(name=file.name, status=file.status, nr_protokol=file.nr_protokol, subdir=file.subdir,
                                   path=file.path)
                file_2.name_of_file_in_the_table = file_name
                file_2.name_of_the_plan = value
                file_2.index = index
                new_list_of_file.append(file_2)
    return new_list_of_file


def file_excel_open_get_date(file_name: str) -> dict | None:
    with (open(file_name, "rb") as f):
        try:
            in_mem_file = io.BytesIO(f.read())
        except FileExistsError:
            print('can not open the file')
            return None
        print("open the excel file ", file_name)
        work_book = openpyxl.load_workbook(in_mem_file, read_only=True)
        print("read the work_book ", work_book)
        print("with the sheetnames ", work_book.sheetnames)
        sheet = work_book.active

        column = 1
        while sheet.cell(row=1, column=column).value is not None:
            value = sheet.cell(row=1, column=column).value
            if value == variables.name_of_the_useful_cell_in_the_excel_file:
                break
            column+=1

        i = 2
        dict_files = dict()
        while sheet.cell(row=i, column=1).value is not None:
            name_index = str(sheet.cell(row=i, column=2).value)
            value = str(sheet.cell(row=i, column=column).value)
            value = '' if value == 'None' else value
            i += 1
            dict_files[name_index] = value
        work_book.close()
    return dict_files


def read_the_setting_from_the_file(path: str) -> dict[Settings, Any] | None:
    try:
        # Open and read the file
        with open(path, 'r') as file:
            content = file.read()
        # Try to parse the content as JSON
        try:
            data_dict = json.loads(content)
            print("JSON data successfully parsed as dictionary:")
            print(data_dict)
            if Settings.dir_for_save.value not in data_dict:
                data_dict[Settings.dir_for_save.value] = variables.new_local_folder
            return {Settings.dir_for_checking: data_dict[Settings.dir_for_checking.value],
                    Settings.year: data_dict[Settings.year.value],
                    Settings.project: data_dict[Settings.project.value],
                    Settings.show_static: data_dict[Settings.show_static.value],
                    Settings.my_projects: data_dict[Settings.my_projects.value],
                    Settings.dir_for_save: data_dict[Settings.dir_for_save.value]}
        except json.JSONDecodeError:
            print("The file content is not valid JSON.")
            return None
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def make_default_settings(path: Path) -> dict | None:
    print(f"The file does not exist at: {path}")

    dir_0 = Path(variables.dir_for_checking)

    list_of_years = sorted(
        folder.name
        for folder in get_only_folders(dir_0)
        if folder.name.startswith(variables.name_of_the_folder.name)
    )

    current_year = list_of_years[-1]

    current_list_of_files_for_the_year = get_only_folders(
        dir_0 / current_year
    )

    project = current_list_of_files_for_the_year[0].name

    settings_0 = {
        Settings.dir_for_checking.value: variables.dir_for_checking,
        Settings.year.value: current_year,
        Settings.my_projects.value: project,
        Settings.show_static.value: False,
        Settings.dir_for_save.value: variables.new_local_folder,
    }

    try:
        path.write_text(
            json.dumps(settings_0, indent=4),
            encoding="utf-8",
        )
        print(f"Dictionary saved as JSON to '{path}'.")
    except Exception as e:
        print(f"Failed to save JSON: {e}")

    return settings_0