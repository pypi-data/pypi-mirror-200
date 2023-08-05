from termcolor import cprint
from PIL import Image
import numpy
import sys
import pathlib
from .base import CommandBase
from ..errors import ArgumentError
import umsgpack


# RGB332 code taken from
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/spritesheet-to-rgb332.py
# Thanks to the pimoroni team for this and so many other things.


class CommandPrepareImage(CommandBase):
    description = 'prepare a 128x128 sprite image for use with the pico'
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

        image = Image.open(filename)
        w, h = image.size
        if w != 128 and h != 128:
            raise ArgumentError("Image must be 128x128 pixels")

        if image_type == 'rgb332':
            try:
                output_filename = filename.with_suffix(".rgb332")
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
            except Exception as e:
                print(e)

        if image_type == 'python':
            try:
                output_filename = filename.with_suffix(".bin")
                converted_image = image.convert('P', palette=Image.ADAPTIVE, colors=16)
                palette = [list(color) for color in list(converted_image.palette.colors.keys())]
                sprite = numpy.array(converted_image).tolist()
                output = {'p': palette, 's': sprite}
                output = umsgpack.dumps(output)

                print(f"Converted: {w}x{h} {len(output)} bytes")

                with open(output_filename, "wb") as f:
                    f.write(output)

                print(f"Written to: {output_filename}")
            except Exception as e:
                print(e)
