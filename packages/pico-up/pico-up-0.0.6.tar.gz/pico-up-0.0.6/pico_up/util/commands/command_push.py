import os
import time
from termcolor import cprint
from .base import CommandBase
from .command_build import CommandBuild
from .command_wipe import CommandWipe


class CommandPush(CommandBase):
    description = 'push local application code to a connected pico'
    options = ['push build: run the build command and push built code to the pico']

    @staticmethod
    def execute(configuration, arguments=None):
        device_address = configuration['device']['address']

        try:
            if arguments[0] == 'build':
                CommandBuild.execute(configuration, arguments)
                os.chdir('build')
        except IndexError:
            pass

        CommandWipe.execute(configuration, arguments)
        cprint('waiting for device', 'blue')
        time.sleep(2.0)
        cprint('pushing local code to device', 'blue')

        ignores = []
        try:
            ignores = configuration['code']['ignores'].split('\n')
            ignores = list(filter(lambda x: x != '', ignores))
        except KeyError:
            pass

        os.system(f'mpremote connect {device_address} mkdir app')
        for root, dirs, files in os.walk("app", topdown=True):
            for name in files:
                remote_name = os.path.join(root, name).replace('\\', '/')
                if not name.endswith(tuple(ignores)):
                    os.system(f'mpremote connect {device_address} cp {remote_name} :{remote_name}')
            for name in dirs:
                remote_name = os.path.join(root, name).replace('\\', '/')
                os.system(f'mpremote connect {device_address} mkdir {remote_name}')

        os.system(f'mpremote connect {device_address} cp main.py :main.py')
        os.system(f'mpremote connect {device_address} cp settings.py :settings.py')
        os.system(f'mpremote connect {device_address} reset')
