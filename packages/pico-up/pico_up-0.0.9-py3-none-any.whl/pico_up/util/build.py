import os

from termcolor import cprint


def minify_python(directory):
    cprint('minifying application code', 'blue')
    cwd = os.getcwd()
    os.chdir(directory)
    os.system('pyminify . --in-place')
    os.chdir(cwd)


def compile_python(directory):
    cprint('compiling application code', 'blue')
    cwd = os.getcwd()
    os.chdir(directory)
    for root, dirs, files in os.walk("app", topdown=True):
        for name in files:
            if name.endswith('.py'):
                original_name = os.path.join(root, name).replace('\\', '/')
                os.system(f'mpy-cross-v6 {original_name}')
                compiled_name = original_name.replace('.py', '.mpy')
                original_size = os.stat(original_name).st_size
                compiled_size = os.stat(compiled_name).st_size
                chosen_file = compiled_name if compiled_size < original_size else original_name
                saved_size = original_size - compiled_size if compiled_size < original_size \
                    else compiled_size - original_size
                print(f'{chosen_file} saving {saved_size} bytes')
                os.remove(compiled_name if original_name == chosen_file else original_name)
    os.chdir(cwd)
