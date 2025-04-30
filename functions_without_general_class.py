import os
import shutil

import variables
from class_file import StatusFile, ClassFile


def get_list_of_all_protocols(dir_protocols: str) -> [str]:
    all_files = get_only_files(path=dir_protocols)
    docx_files = {x[:-5] for x in all_files if x[-5:] == '.docx'}
    doc_files = {x[:-4] for x in all_files if x[-4:] == '.doc'}
    filter_files = doc_files | docx_files
    filter_files_2 = set()
    for variant_of_protocol in variables.names_of_protocol:
        for file_name_i in filter_files:
            if variant_of_protocol in file_name_i:
                n = file_name_i.index(variant_of_protocol)
                file_filter_name = file_name_i[n + len(variant_of_protocol):]
                filter_files_2.add(file_filter_name)
    send_protocols = []
    not_send_protocols = []
    for protokol_i in filter_files_2:
        if protokol_i.isnumeric():
            send_protocols.append(variables.protocol + '_' + protokol_i)
        else:
            not_send_protocols.append(variables.protocol + protokol_i)
    if len(not_send_protocols) == 0:
        not_send_protocols = [variables.protocol + '_' + '00']
    return not_send_protocols, send_protocols


def start_file_is_send(path: str, name: str, subdir: str):
    path = path.replace('\\' + name, '')
    if subdir != '':
        path = path.replace('\\' + subdir, '')
    path = path.replace(variables.incoming_docs, variables.checked_files)
    all_files = get_only_files(path=path)
    for ending in variables.variants_of_the_ending:
        name_i = name.replace('.pdf', '_' + ending + '.pdf')
        if name_i in all_files:
            path += '\\' + name_i
            start_the_file(path=path)


def check_the_file(name: str, dict_i: dict, folder: str, status_name: str) -> tuple[str, str] | bool:
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


def get_dict_to_send_files(path: str, dict_checked_files: dict) -> dict:
    if len(dict_checked_files) == 0:
        return dict()
    path = path + '\\' + variables.checked_files
    all_folder = get_only_folders(path=path)
    if variables.files_to_send not in set(all_folder):
        print('no subdir', variables.files_to_send)
        return {}
    path = path + '\\' + variables.files_to_send
    all_folder = get_only_folders(path=path)
    return get_dict_with_protocol_files(path=path, folders=all_folder)


def get_dict_checked_files(path: str, dict_by_checking: dict) -> dict:
    if len(dict_by_checking) == 0:
        return dict()
    path = path + '\\' + variables.checked_files
    all_folder = get_only_folders(path=path)
    if variables.checked_files_planes not in set(all_folder):
        print('no subdir', variables.checked_files_planes)
        return {}
    path = path + '\\' + variables.checked_files_planes
    all_folder = get_only_folders(path=path)
    return get_dict_with_protocol_files(path=path, folders=all_folder)


def get_dict_of_by_checking_files(path: str) -> dict:
    all_folder = get_only_folders(path=path)
    if variables.checked_files not in set(all_folder):
        print('no subdir !!', variables.checked_files)
        return {}
    path = path + '\\' + variables.checked_files
    all_folder = get_only_folders(path=path)
    if variables.by_checking not in set(all_folder):
        print('no subdir', variables.by_checking)
        return {}
    path = path + '\\' + variables.by_checking
    all_folder = get_only_folders(path=path)
    return get_dict_with_protocol_files(path=path, folders=all_folder)


def get_dict_with_protocol_files(path: str, folders: [str]) -> dict:
    only_files = get_only_files(path=path)
    # all files in folders
    dict_protokol_files = {0: only_files}

    for folder_i in folders:
        for name_i in variables.names_of_protocol:
            if folder_i.find(name_i) != -1:

                nummer_i = folder_i.replace(name_i, '')
                try:
                    nummer_i = int(nummer_i)
                except:
                    print('there is no number', folder_i)
                    break
                path_i = path + '\\' + folder_i
                dict_protokol_files[nummer_i] = dict()
                dict_protokol_files[nummer_i][0] = get_only_files(path=path_i)
                folders_ii = get_only_folders(path=path_i)
                for folder_j in folders_ii:
                    path_j = path_i + '\\' + folder_j
                    dict_protokol_files[nummer_i][folder_j] = get_only_files(path=path_j)
                continue
    return dict_protokol_files


def get_list_of_send_files(path: str) -> [str]:
    all_folder = get_only_folders(path=path)
    if variables.checked_files not in set(all_folder):
        print('no subdir', variables.checked_files)
        return []
    path = path + '\\' + variables.checked_files
    row_list = get_only_files(path=path)
    list_of_files = []
    for file in row_list:
        if file[-4:] == '.pdf':
            file = file[:-4]
            for n in [7, 6, 4]:
                if file[-n:] in variables.variants_of_the_ending:
                    list_of_files.append(file[:-(n + 1)])
                    break
    return list_of_files


def get_only_folders(path: str) -> [str]:
    """print("Only directories:")
    print([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
    print("\nOnly files:")
    print([name for name in os.listdir(path) if not os.path.isdir(os.path.join(path, name))])
    print("\nAll directories and files :")
    print([name for name in os.listdir(path)])"""
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


def get_only_files(path: str) -> [str]:
    return [name for name in os.listdir(path) if not os.path.isdir(os.path.join(path, name))]


def start_file_by_status(path: str, name: str, protokol_nr: int, folder_to_check: str, subdir: str):
    path = path.replace(variables.incoming_docs, variables.checked_files + '\\' + folder_to_check)
    path = path.replace(name, '')
    if subdir != '':
        path = path.replace('\\' + subdir, '')
    all_folder = get_only_folders(path=path)
    for name_i in variables.names_of_protocol:
        name_of_the_protocol = name_i + str(protokol_nr)
        if name_of_the_protocol in all_folder:
            if path[-1:] == "\\":
                path = path[:-1]
            path += '\\' + name_of_the_protocol
            if subdir != '':
                path += '\\' + subdir
            all_files = get_only_files(path=path)
            if name in all_files:
                path += '\\' + name
                start_the_file(path=path)


def start_the_file(path: str):
    os.startfile(path)


def copy_the_file(old_path: str, new_path: str, name: str):
    print('I copy the file', name)
    print('from', old_path)
    print('to', new_path)
    print('---->>>>>')

    if os.path.isfile(old_path) is False:
        print('there is no file', name)
        return None
    new_path_for_the_folder = new_path.replace(name, '')
    if not os.path.exists(new_path_for_the_folder):
        os.makedirs(new_path_for_the_folder)
    try:
        shutil.copyfile(old_path, new_path)
    except Exception as err:
        print('copy error', name)
        print(f"Unexpected {err=}, {type(err)=}")
        raise



def move_from_unchecked_to_by_checking(file: ClassFile, protocol: str = ''):
    old_path = file.path
    if protocol == '':
        new_part = variables.checked_files + '\\' + variables.by_checking
    else:
        new_part = variables.checked_files + '\\' + variables.by_checking + '\\' + protocol
    new_path = file.path.replace(variables.incoming_docs, new_part)
    file.status = StatusFile.by_checking
    copy_the_file(old_path=old_path, new_path=new_path, name=file.name)


def move_from_by_checking_to_checked(file: ClassFile, protocol: str = ''):
    if protocol == '':
        new_part = variables.checked_files + '\\' + variables.by_checking
    else:
        new_part = variables.checked_files + '\\' + variables.by_checking + '\\' + protocol
    old_path = file.path.replace(variables.incoming_docs, new_part)

    if protocol == '':
        new_part = variables.checked_files + '\\' + variables.checked_files_planes
    else:
        new_part = variables.checked_files + '\\' + variables.checked_files_planes + '\\' + protocol
    new_path = file.path.replace(variables.incoming_docs, new_part)
    copy_the_file(old_path=old_path, new_path=new_path, name=file.name)
    file.status = StatusFile.checked


def move_from_checked_to_to_send(file: ClassFile, protocol: str = ''):
    if protocol == '':
        new_part = variables.checked_files + '\\' + variables.checked_files_planes
    else:
        new_part = variables.checked_files + '\\' + variables.checked_files_planes + '\\' + protocol
    old_path = file.path.replace(variables.incoming_docs, new_part)
    if protocol == '':
        new_part = variables.checked_files + '\\' + variables.files_to_send
    else:
        new_part = variables.checked_files + '\\' + variables.files_to_send + '\\' + protocol
    new_path = file.path.replace(variables.incoming_docs, new_part)
    copy_the_file(old_path=old_path, new_path=new_path, name=file.name)
    file.status = StatusFile.to_send


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
