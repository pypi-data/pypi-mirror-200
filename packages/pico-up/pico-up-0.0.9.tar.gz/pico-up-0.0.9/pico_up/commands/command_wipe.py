from termcolor import cprint
import os
import re
import subprocess

from .base import CommandBase
from ..util.configuration import Configuration


class CommandWipe(CommandBase):
    description = 'remove all files from a connected pico'

    @staticmethod
    def execute(configuration: Configuration, arguments=None):
        cprint('wiping all code currently stored on device', 'red')

        def get_command_list(root=''):
            wipe_command_list = []

            output = subprocess.check_output(f"mpremote connect {configuration.device.address} ls {root}", shell=True)

            for line in output.decode('utf-8').split(os.linesep):
                if not line or line.startswith('ls'):
                    continue
                line_path = re.search(r'\d+\s(.+)', line.strip()).group(1)
                if line_path.endswith('/'):
                    wipe_command_list += get_command_list(f'{root}{line_path}')
                wipe_command_list.append(f'mpremote connect {configuration.device.address} rm {root}{line_path}')

            return wipe_command_list

        for wipe_command in get_command_list():
            os.system(wipe_command)

        os.system(f'mpremote connect {configuration.device.address} reset')
