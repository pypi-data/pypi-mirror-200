from termcolor import cprint
from .commands import available_commands


class CommandHelp:
    description = 'show general help or specific command help'

    @staticmethod
    def execute(configuration, arguments=None):
        if arguments:
            name = arguments[0]
            try:
                command = available_commands.get(name)
                cprint(f'command: {name} - {command.description}', 'blue')
                if len(command.options) > 0:
                    print()
                    cprint('optional arguments:', 'blue')
                    cprint("\n".join(command.options))
            except AttributeError:
                cprint(f'command {name} does not exist', 'red')
                CommandHelp.execute(configuration, arguments)
        else:
            cprint('python pico-up', 'blue')
            print()
            for name in available_commands.keys():
                command = available_commands.get(name)
                cprint(f'{name.ljust(7)} {command.description}')
        print()
