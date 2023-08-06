import os
from termcolor import cprint
from .base import CommandBase


class CommandVersion(CommandBase):
    description = 'show the version of pico-up'

    @staticmethod
    def execute(configuration, arguments=None):
        output = os.popen('pip list').read()
        version = 'dev'
        for item in output.split('\n'):
            if item.startswith('pico-up'):
                version = item.split(' ')[-1]

        cprint(f'pico-up version {version}', 'blue')
