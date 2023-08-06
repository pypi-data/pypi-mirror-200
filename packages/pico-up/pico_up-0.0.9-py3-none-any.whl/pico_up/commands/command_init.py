import os
from termcolor import cprint
from .base import CommandBase

__BASE_CONFIG_FILE__ = '''
[device]
address = '/dev/ttyACM0'

[push]
ignores =
        .jpg
        .rgb332
        .bin

modules =
        pico_up_modules.msgpack_loads
'''


class CommandInit(CommandBase):
    description = 'initialise a python pico project in the current directory'

    @staticmethod
    def execute(configuration, arguments=None):
        cprint('creating a README file', 'blue')
        try:
            f = open("README.md", "x")
            f.write("# My Pico Project\n")
            f.close()
        except FileExistsError:
            cprint('README file already exists', 'red')

        cprint('creating a .gitignore', 'blue')
        try:
            f = open(".gitignore", "x")
            f.write("\n".join([
                '*.mpy',
                'build/',
            ]))
            f.close()
        except FileExistsError:
            cprint('.gitignore file already exists', 'red')

        cprint('creating settings file', 'blue')
        try:
            f = open("settings.py", "x")
            f.write("screen = 'unicorn'\n")
            f.close()
        except FileExistsError:
            cprint('settings file already exists', 'red')

        cprint('creating main entrypoint', 'blue')
        try:
            f = open("main.py", "x")
            f.write("print('Hello!')\n")
            f.close()
        except FileExistsError:
            cprint('main.py file already exists', 'red')

        cprint('creating application module', 'blue')
        try:
            os.mkdir('app')
        except FileExistsError:
            cprint('app directory already exists', 'red')

        try:
            f = open("app/__init__.py", "x")
            f.write("\n")
            f.close()
        except FileExistsError:
            cprint('app module file already exists', 'red')

        cprint('creating a .pico-up.ini file', 'blue')
        try:
            f = open(".pico-up.ini", "x")
            f.write(__BASE_CONFIG_FILE__)
            f.close()
        except FileExistsError:
            cprint('.pico-up.ini file already exists', 'red')
