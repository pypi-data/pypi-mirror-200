import configparser
from .util import commands, CommandHelp
from termcolor import cprint
import sys
from .util.errors import ArgumentError


def main():
    try:
        args = sys.argv[1:]
        process_command(args[0], args[1:])
    except IndexError:
        cprint('No command given', 'red')
        print()
        CommandHelp.execute({})


def process_command(command=None, arguments=None):
    if command == 'init':
        configuration = {}
    else:
        configuration = load_configuration()

    try:
        if command in commands.available_commands.keys():
            commands.available_commands.get(command).execute(configuration, arguments)
        else:
            CommandHelp.execute(configuration, arguments)
    except ArgumentError as e:
        cprint(f'error: {e}', 'red')
        CommandHelp.execute(configuration, [command])


def load_configuration():
    try:
        pico_config = configparser.ConfigParser()
        pico_config.read('.pico-up.ini')
        try:
            test = pico_config['device']['address']
        except KeyError:
            cprint('config found, but missing sections', 'red')
            quit(101)

        return pico_config
    except FileNotFoundError:
        cprint('no configuration file found', 'red')
        quit(100)
