import os
import shutil
import time
from termcolor import cprint
from .base import CommandBase
from .command_wipe import CommandWipe
from ..util.build import minify_python, compile_python
from ..util.configuration import Configuration
from ..util.files import get_application_files, get_folders_to_create_for_files, get_module_files, \
    create_staging_directory


class CommandPush(CommandBase):
    description = 'push local application code to a connected pico'
    options = ['push: attempt to create the smallest possible set of files to deploy',
               'push dev: push all application files as they exist without reducing size']

    @staticmethod
    def execute(configuration: Configuration, arguments=None):
        is_dev_build = False
        try:
            if arguments[0] == 'dev':
                is_dev_build = True
        except IndexError:
            pass

        modules_to_push = configuration.push.modules
        modules_to_push.append('pico_up_modules.free_commands')
        modules_to_push = get_module_files(modules_to_push)
        application_files = get_application_files(ignores=configuration.push.ignores)
        staging_directory, delete_staging_directory = create_staging_directory()

        for directory in get_folders_to_create_for_files(application_files):
            os.mkdir(os.path.join(staging_directory, directory))

        for file in application_files:
            shutil.copyfile(file, os.path.join(staging_directory, file))

        os.mkdir(os.path.join(staging_directory, 'app/mods'))
        f = open(os.path.join(staging_directory, 'app/mods/__init__.py'), 'x')
        f.close()

        for module in modules_to_push:
            shutil.copyfile(module, os.path.join(staging_directory, 'app/mods', os.path.basename(module)))

        if not is_dev_build:
            minify_python(staging_directory)
            compile_python(staging_directory)

        files_to_upload = get_application_files(search_in=staging_directory)
        directories_to_upload = get_folders_to_create_for_files(files_to_upload)

        CommandWipe.execute(configuration, arguments)
        cprint('waiting for device', 'blue')
        time.sleep(1.0)
        cprint('pushing local code to device', 'blue')

        cwd = os.getcwd()
        os.chdir(staging_directory)

        for directory in directories_to_upload:
            os.system(f'mpremote connect {configuration.device.address} mkdir {directory}')

        for file in files_to_upload:
            os.system(f'mpremote connect {configuration.device.address} cp {file} :{file}')

        os.chdir(cwd)

        delete_staging_directory()

        os.system(f'mpremote connect {configuration.device.address} reset')
