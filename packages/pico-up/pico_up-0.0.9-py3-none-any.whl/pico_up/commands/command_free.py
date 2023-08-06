import os
from termcolor import cprint
from .base import CommandBase


class CommandFree(CommandBase):
    description = 'show the current free ram and rom space, requires a soft-reset'

    @staticmethod
    def execute(configuration, arguments=None):
        cprint(f'getting free ram and rom space', 'blue')
        cprint('this will terminate your application, press enter to proceed', 'yellow')
        input()
        os.system(f'mpremote resume exec "from app.mods.free_commands import rom_space, ram_space; '
                  f'rom_space(); ram_space();"')
