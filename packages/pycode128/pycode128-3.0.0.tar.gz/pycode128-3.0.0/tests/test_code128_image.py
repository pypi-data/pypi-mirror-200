#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Tests for `code128_image` module."""

from pathlib import Path

from PIL import Image, ImageChops

from pycode128.code128_image import Code128Image
from pycode128.pycode128 import PyCode128


def test_changing_image_bar_width():
    """Test image with different bar width."""
    _code128 = PyCode128('test')
    _code128.encode_raw()
    _image = Code128Image(_code128.encoded_data, bar_width=10)

    _image_expected = Image.open(Path.cwd().joinpath("tests").joinpath("image_width_10.png"))
    _diff = ImageChops.difference(_image.get_image(), _image_expected)
    assert not _diff.getbbox()


def test_changing_image_height():
    """Test image with different height."""
    _code128 = PyCode128('test')
    _code128.encode_raw()
    _image = Code128Image(_code128.encoded_data, image_height=100)

    _image_expected = Image.open(Path.cwd().joinpath("tests").joinpath("image_height_100.png"))
    _diff = ImageChops.difference(_image.get_image(), _image_expected)
    assert not _diff.getbbox()


def test_compare_image():
    """Compare image with existing one."""
    _code128 = PyCode128('test')
    _code128.encode_raw()
    _image_gen = Code128Image(_code128.encoded_data)
    _image_expected = Image.open(Path.cwd().joinpath("tests").joinpath("test_image.png"))
    _diff = ImageChops.difference(_image_gen.get_image(), _image_expected)
    assert not _diff.getbbox()


def test_compare_image_fnc3():
    """Compare image with existing one."""
    _code128 = PyCode128('[FNC3] $P\r')
    _code128.encode_raw()
    _image_gen = Code128Image(_code128.encoded_data)
    _image_expected = Image.open(Path.cwd().joinpath("tests").joinpath("fnc3_dollar_p.png"))
    _diff = ImageChops.difference(_image_gen.get_image(), _image_expected)
    assert not _diff.getbbox()


def test_compare_image_action_label():
    """Compare image with existing one."""
    _code128 = PyCode128('[FNC3] RevA\r')
    _code128.encode_raw()
    _image_gen = Code128Image(_code128.encoded_data)
    _image_expected = Image.open(Path.cwd().joinpath("tests").joinpath("action_label.png"))
    _diff = ImageChops.difference(_image_gen.get_image(), _image_expected)
    assert not _diff.getbbox()
