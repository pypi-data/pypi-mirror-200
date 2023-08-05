from termcolor import cprint
from PIL import Image
import numpy
import sys
import pathlib
from .base import CommandBase
from ..errors import ArgumentError

# RGB332 code taken from
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/spritesheet-to-rgb332.py
# Thanks to the pimoroni team for this and so many other things.


class CommandPrepareImage(CommandBase):
    description = 'prepare an image for use with the pico'
    options = ['python [filename]: convert image to a python file with pixels and palette',
               'rgb332 [filename]: convert image to an rgb332 file']

    @staticmethod
    def execute(configuration, arguments=None):
        try:
            image_type = arguments[0]
            filename = pathlib.Path(arguments[1])
        except IndexError:
            cprint('type or filename were not set', 'red')
            raise ArgumentError

        try:
            ['rgb332', 'python'].index(image_type)
        except ValueError:
            cprint('type is not valid', 'red')
            raise ArgumentError

        if image_type == 'rgb332':
            image = Image.open(filename)
            output_filename = filename.with_suffix(".rgb332")
            w, h = image.size
            pb = numpy.array(image.convert('RGBA')).astype('uint16')
            r = (pb[:, :, 0] & 0b11100000) >> 0
            g = (pb[:, :, 1] & 0b11100000) >> 3
            b = (pb[:, :, 2] & 0b11000000) >> 6
            a = pb[:, :, 3]  # Discarded
            color = r | g | b
            output = color.astype("uint8").flatten().tobytes()
            print(f"Converted: {w}x{h} {len(output)} bytes")

            with open(output_filename, "wb") as f:
                f.write(output)

            print(f"Written to: {output_filename}")

        if image_type == 'python':
            image = Image.open(filename)
            output_filename = filename.with_suffix(".py")
            w, h = image.size
            sprite = numpy.array(image.convert('RGB')).tolist()
            flattened_sprite = [item for sublist in sprite for item in sublist]

            palette_set = set()
            for item in flattened_sprite:
                palette_set.add(f'{item[0]},{item[1]},{item[2]}')

            palette = []
            for item in list(palette_set):
                rgb = []
                for c in item.split(','):
                    rgb.append(int(c))
                palette.append(rgb)

            palette_sprite = [[None] * 7 for i in range(7)]
            for y, row in enumerate(sprite):
                for x, column in enumerate(row):
                    palette_sprite[x][y] = palette.index(column)

            output = f"s = {palette_sprite}\np = {palette}\n"

            print(f"Converted: {w}x{h} {len(output)} bytes")

            with open(output_filename, "w") as f:
                f.write(output)

            print(f"Written to: {output_filename}")
