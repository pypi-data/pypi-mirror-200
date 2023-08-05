import os
import shutil

from termcolor import cprint

from .base import CommandBase


class CommandBuild(CommandBase):
    description = 'minify and attempt to compile pico application to bytecodes'

    @staticmethod
    def execute(configuration, arguments=None):
        cprint('copying codebase to build', 'blue')
        try:
            shutil.rmtree('build')
        except FileNotFoundError:
            pass
        os.mkdir('build')
        shutil.copytree('app', 'build/app')
        shutil.copyfile('main.py', 'build/main.py')
        shutil.copyfile('settings.py', 'build/settings.py')
        cprint('minifying codebase', 'blue')
        os.system('pyminify build --in-place')
        cprint('cross-compiling application libraries', 'blue')
        os.chdir('build')
        for root, dirs, files in os.walk("app", topdown=True):
            for name in files:
                if name.endswith('.py'):
                    original_name = os.path.join(root, name).replace('\\', '/')
                    os.system(f'mpy-cross-v6 {original_name}')
                    compiled_name = original_name.replace('.py', '.mpy')
                    original_size = os.stat(original_name).st_size
                    compiled_size = os.stat(compiled_name).st_size
                    chosen_file = compiled_name if compiled_size < original_size else original_name
                    saved_size = original_size - compiled_size if compiled_size < original_size else compiled_size - original_size
                    print(f'{chosen_file} saving {saved_size} bytes')
                    os.remove(compiled_name if original_name == chosen_file else original_name)
        os.chdir('..')
