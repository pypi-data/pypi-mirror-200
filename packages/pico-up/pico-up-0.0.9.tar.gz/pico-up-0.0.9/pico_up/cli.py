import configparser
import pico_up.commands
from termcolor import cprint
import sys
from .command_help import CommandHelp
from .util.configuration import load_configuration
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
        if command in pico_up.commands.available_commands.keys():
            pico_up.commands.available_commands.get(command).execute(configuration, arguments)
        else:
            CommandHelp.execute(configuration, arguments)
    except ArgumentError as e:
        cprint(f'error: {e}\n', 'red')
        CommandHelp.execute(configuration, [command])
