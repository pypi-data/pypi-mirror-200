from termcolor import cprint
from PIL import Image
import numpy
import pathlib
from .base import CommandBase
from pico_up.util.errors import ArgumentError
import umsgpack


# RGB332 code taken from
# https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/spritesheet-to-rgb332.py
# Thanks to the pimoroni team for this and so many other things.


class CommandPrepareImage(CommandBase):
    description = 'prepare a 128x128 sprite image for use with the pico'
    options = ['python [filename] <sprite size>: convert image to a python file with pixels and palette, ',
               '                                 optionally reduce each sprites size',
               'rgb332 [filename]: convert image to an rgb332 file']

    @staticmethod
    def execute(configuration, arguments=None):
        try:
            image_type = arguments[0]
            filename = pathlib.Path(arguments[1])
            sprite_size = 8
            try:
                sprite_size = int(arguments[2])
                if sprite_size > 8:
                    raise ArgumentError('a sprite cannot be enlarged, only shrunk')
            except IndexError:
                pass
            except TypeError:
                pass
        except IndexError:
            raise ArgumentError('Image type or filename were not set')

        try:
            ['rgb332', 'python'].index(image_type)
        except ValueError:
            raise ArgumentError('Image type is not valid')

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
                w, h = image.size
                print(f"Converted: {w}x{h} {len(output)} bytes")

                with open(output_filename, "wb") as f:
                    f.write(output)

                print(f"Written to: {output_filename}")
            except Exception as e:
                print(e)

        if image_type == 'python':
            try:
                output_filename = filename.with_suffix(".bin")
                converted_image = image.convert('P', palette=Image.ADAPTIVE, colors=32)
                palette = [list(color) for color in list(converted_image.palette.colors.keys())]
                sprite = numpy.array(converted_image).tolist()

                final_size = sprite_size * 16
                if final_size != 128:
                    sprite = _resize_sprite_sheet(sprite, 8, sprite_size)

                output = {'p': palette, 's': sprite, 'd': sprite_size}
                output = umsgpack.dumps(output)
                print(f"Converted: {len(sprite)}x{len(sprite[0])} {len(output)} bytes")

                with open(output_filename, "wb") as f:
                    f.write(output)

                print(f"Written to: {output_filename}")
            except Exception as e:
                print(e)


def _resize_sprite_sheet(input_sprite_sheet, current_sprite_size, new_sprite_size):
    sprites_per_row = int(len(input_sprite_sheet) / current_sprite_size)
    new_sprite_sheet = [[0] * new_sprite_size * sprites_per_row for _ in range(new_sprite_size * sprites_per_row)]
    new_sprite_sheet = numpy.array(new_sprite_sheet)
    input_sprite_sheet = numpy.array(input_sprite_sheet)

    sprites = []
    for x in range(sprites_per_row):
        for y in range(sprites_per_row):
            sprites.append(
                input_sprite_sheet[
                    current_sprite_size * x:current_sprite_size * x + current_sprite_size,
                    current_sprite_size * y:current_sprite_size * y + current_sprite_size,
                ].tolist()
            )

    for reduction in range(current_sprite_size - new_sprite_size):
        sprite_mid_point = int((current_sprite_size - reduction - 1) / 2)
        for sprite in sprites:
            del sprite[sprite_mid_point]
            for row in sprite:
                del row[sprite_mid_point]

    current_sprite = 0
    for x in range(sprites_per_row):
        for y in range(sprites_per_row):
            new_sprite_sheet[
                x * new_sprite_size:x * new_sprite_size + new_sprite_size,
                y * new_sprite_size:y * new_sprite_size + new_sprite_size
            ] = sprites[current_sprite]
            current_sprite += 1

    return new_sprite_sheet.tolist()
