# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Class to retrieve a Pillow Image from byte buffer."""

from itertools import repeat

from PIL import Image


class Code128Image:  # pylint: disable=too-few-public-methods
    """Class to convert byte buffer to PIL Image."""

    def __init__(self, byte_buffer: bytes, image_height: int = 200, bar_width: int = 5):
        """Initialization.

        Arguments:
            byte_buffer: byte buffer from PyCode128 C extension.
            image_height: height of final image
            bar_width: width of each single bar
        """
        self.__image_height = image_height
        self.__bar_width = bar_width

        # Once you get barcode_data, each byte corresponds to whether a vertical line should be drawn.
        # If the byte is 0xff, then draw a line. If the byte is 0x00, then don't.
        self.__bytes = byte_buffer.replace(b'\x00', b'\x01').replace(b'\xff', b'\x00').replace(b'\x01', b'\xff')

    def get_image(self) -> Image:
        """Retrieve PIL image.

        Returns:
            PIL Image object.
        """
        _cols = b''.join(map(lambda x: bytes(repeat(x, self.__bar_width)), self.__bytes))
        _image_width = len(_cols)
        _image_bytes = b''.join(repeat(_cols, self.__image_height))
        _image = Image.frombuffer(mode="L", size=(_image_width, self.__image_height), data=_image_bytes)
        return _image
