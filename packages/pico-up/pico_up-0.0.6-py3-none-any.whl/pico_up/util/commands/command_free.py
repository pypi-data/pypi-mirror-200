import os

from termcolor import cprint
from .base import CommandBase


class CommandFree(CommandBase):
    description = 'show the current free ram and rom space, requires a soft-reset'

    @staticmethod
    def execute(configuration, arguments=None):
        cprint(f'getting free ram and rom space', 'blue')
        device = configuration['device']['address']
        os.system(f'mpremote connect {device} run main.py')
        cprint(f'device has been reset, do something then press enter to get free resources', 'blue')
        input()
        command = "import os;f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, _, _, _, _, _ = os.statvfs('//');print('ROM: {0} Total {1} Free ({2:.2f}%)'.format(f_frsize * f_blocks, f_bsize * f_bfree, ((f_bsize * f_bfree) / (f_frsize * f_blocks)) * 100));"
        os.system(f'mpremote resume exec "{command}"')

        command = "import gc;F=gc.mem_free();A=gc.mem_alloc();T=F+A;P='{0:.2f}%'.format(F / T * 100);print('RAM: {0} Total {1} Free ({2})'.format(T, F, P));"
        os.system(f'mpremote resume exec "{command}"')
