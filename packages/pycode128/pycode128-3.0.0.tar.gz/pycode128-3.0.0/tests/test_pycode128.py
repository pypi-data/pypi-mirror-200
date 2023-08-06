#!/usr/bin/env python

# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Tests for `pycode128` package."""

import pytest

from pycode128.pycode128 import PyCode128


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_object_creation():
    """Test PyCode128 object creation."""
    _code128 = PyCode128('test')
    assert _code128.input_data == 'test'
    assert _code128.__doc__ == "PyCode128 object"

    assert _code128.length == 0
    assert _code128.encoded_data == ""

    _dir_code128 = dir(_code128)
    # methods
    assert 'encode_gs1' in _dir_code128
    assert 'encode_raw' in _dir_code128
    assert 'estimate_len' in _dir_code128

    # properties
    assert 'encoded_data' in _dir_code128
    assert 'input_data' in _dir_code128
    assert 'length' in _dir_code128


def test_object_creation_with_keyword():
    """Test PyCode128 object creation."""
    _code128 = PyCode128(input_data='test')
    assert _code128.input_data == 'test'
    assert _code128.__doc__ == "PyCode128 object"

    assert _code128.length == 0
    assert _code128.encoded_data == ""


def test_object_deletion():
    """Test PyCode128 object deletion."""
    _code128 = PyCode128('test')
    assert _code128.input_data == 'test'

    # delete object, accessing to it must raise NameError
    # C framework should check not freed memory
    del _code128
    with pytest.raises(NameError):
        _code128.input_data  # noqa: F821


def test_attribute_deletion():
    """Test PyCode128 attribute deletion."""
    _code128 = PyCode128('test')
    with pytest.raises(TypeError):
        del _code128.input_data


def test_empty_creation():
    """Test PyCode128 object empty init."""
    with pytest.raises(TypeError):
        _ = PyCode128()


def test_change_input_data():
    """Test PyCode128 object change input data."""
    _code128 = PyCode128('test')
    assert _code128.input_data == 'test'
    _code128.input_data = 'new_test'
    assert _code128.input_data == 'new_test'


def test_set_encoded_data_length():
    """Test PyCode128 object set unsettable members."""
    _code128 = PyCode128('test')
    with pytest.raises(AttributeError):
        _code128.encoded_data = 'should_fail'
    with pytest.raises(AttributeError):
        _code128.length = 'should_fail'


def test_encode_no_arg():
    """Test PyCode128 encode with not necessary argument."""
    _code128 = PyCode128('test')
    with pytest.raises(TypeError):
        _code128.encode_raw('new_arg')
    with pytest.raises(TypeError):
        _code128.encode_gs1('new_arg')


def test_encode_raw():
    """Test encode_raw method."""
    _code128 = PyCode128('test')
    _code128.encode_raw()
    assert _code128.length == 99
    assert isinstance(_code128.encoded_data, bytes)
    assert _code128.length == len(_code128.encoded_data)
    assert (
        _code128.encoded_data == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xff\x00\x00\xff\x00'
        b'\x00\x00\x00\xff\x00\x00\xff\xff\xff\xff\x00\xff\x00\x00\xff\x00\xff\xff'
        b'\x00\x00\xff\x00\x00\x00\x00\xff\x00\xff\xff\xff\xff\x00\x00\xff\x00\x00'
        b'\xff\x00\x00\xff\xff\xff\xff\x00\xff\x00\x00\xff\xff\xff\xff\x00\x00\xff'
        b'\x00\xff\x00\x00\xff\xff\x00\x00\x00\xff\xff\xff\x00\xff\x00\xff\xff\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    )


def test_encode_raw_fnc3():
    """Test encode_raw method."""
    _code128 = PyCode128('[FNC3] $P\r')
    _code128.encode_raw()
    assert _code128.length == 99
    assert isinstance(_code128.encoded_data, bytes)
    assert _code128.length == len(_code128.encoded_data)
    assert (
        _code128.encoded_data == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
        b'\x00\xff\x00\x00\x00\x00\xff\x00\x00\xff\x00\xff'
        b'\xff\xff\xff\x00\x00\x00\xff\x00\xff\x00\x00\xff'
        b'\x00\x00\x00\xff\xff\x00\x00\xff\xff\xff\x00\xff'
        b'\xff\xff\x00\xff\xff\x00\xff\xff\xff\xff\x00\xff'
        b'\xff\xff\x00\xff\x00\xff\xff\x00\x00\x00\xff\x00'
        b'\x00\x00\xff\x00\xff\xff\x00\x00\x00\xff\xff\xff'
        b'\x00\xff\x00\xff\xff\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x00\x00'
    )


def test_encode_raw_action_label():
    """Test encode_raw method."""
    _code128 = PyCode128('[FNC3] RevA\r')
    _code128.encode_raw()
    assert _code128.length == 132
    assert isinstance(_code128.encoded_data, bytes)
    assert _code128.length == len(_code128.encoded_data)
    assert (
        _code128.encoded_data == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
        b'\x00\xff\x00\x00\xff\x00\x00\x00\x00\xff\x00\xff'
        b'\xff\xff\xff\x00\x00\x00\xff\x00\xff\xff\x00\x00'
        b'\x00\xff\x00\xff\xff\xff\x00\xff\x00\xff\xff\x00'
        b'\x00\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\xff'
        b'\x00\x00\xff\x00\x00\xff\x00\xff\x00\x00\x00\xff'
        b'\xff\x00\x00\x00\xff\xff\xff\x00\xff\x00\xff\xff'
        b'\xff\xff\x00\xff\xff\xff\xff\x00\xff\xff\xff\x00'
        b'\xff\x00\xff\xff\xff\x00\xff\x00\xff\xff\xff\xff'
        b'\x00\xff\xff\x00\x00\x00\xff\xff\xff\x00\xff\x00'
        b'\xff\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    )


def test_encode_gs1():
    """Test encode_gs1 method."""
    _code128 = PyCode128('test')
    _code128.encode_gs1()
    assert _code128.length == 99
    assert isinstance(_code128.encoded_data, bytes)
    assert _code128.length == len(_code128.encoded_data)
    assert (
        _code128.encoded_data == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x00\xff\x00\x00\xff\x00'
        b'\x00\x00\x00\xff\x00\x00\xff\xff\xff\xff\x00\xff\x00\x00\xff\x00\xff\xff'
        b'\x00\x00\xff\x00\x00\x00\x00\xff\x00\xff\xff\xff\xff\x00\x00\xff\x00\x00'
        b'\xff\x00\x00\xff\xff\xff\xff\x00\xff\x00\x00\xff\xff\xff\xff\x00\x00\xff'
        b'\x00\xff\x00\x00\xff\xff\x00\x00\x00\xff\xff\xff\x00\xff\x00\xff\xff\x00'
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    )


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.

    Arguments:
        response: pytest feature
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    del response


def test_py_version():
    """Dummy test to print python version used by pytest."""
    import sys

    print(f"in TEST: {sys.version}  -- {sys.version_info}")
    # if sys.version_info <= (3, 9, 18):
    #     # 3.9 OK
    #     assert True
    # else:
    #     # 3.10 FAIL
    #     assert False
