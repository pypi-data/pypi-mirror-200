import os
import tempfile
import time


def get_application_files(search_in=None, ignores=()):
    cwd = None
    if search_in is not None:
        cwd = os.getcwd()
        os.chdir(search_in)

    file_list = ['main.py', 'settings.py']
    for root, dirs, files in os.walk("app", topdown=True):
        for name in files:
            if not name.endswith(tuple(ignores)):
                file_list.append(os.path.join(root, name))

    if search_in is not None:
        os.chdir(cwd)
    return file_list


def get_module_files(modules=()):
    module_files = []
    for module in modules:
        module_file_path, _ = get_module_file(module)
        module_files.append(module_file_path)
    return module_files


def get_folders_to_create_for_files(file_list):
    folders_list = []
    for file in file_list:
        file = file.split('/')
        if len(file) == 1:
            continue
        folders_list.append("/".join(file[:-1]))
    folders_list = list(set(folders_list))
    folders_list.sort()
    return folders_list


def get_files_to_create(modules=()):
    files = []
    if len(modules) > 0:
        files = ['app/mods/__init__.py']
    return files


def get_module_file(module, root=None):
    cwd = None
    if root:
        cwd = os.getcwd()
        os.chdir(root)
    module_file_path = getattr(__import__(module), module.split('.')[-1]).__file__
    module_file_path = os.path.relpath(module_file_path)
    module_file_name = os.path.basename(module_file_path)
    if root:
        os.chdir(cwd)
    return module_file_path, module_file_name


def create_staging_directory():
    folder = tempfile.TemporaryDirectory(prefix=f'pico-up-{int(time.time())}-')
    return folder.name, folder.cleanup
