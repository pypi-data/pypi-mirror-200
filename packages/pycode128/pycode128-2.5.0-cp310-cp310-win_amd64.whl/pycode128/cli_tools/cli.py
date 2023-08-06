# SPDX-FileCopyrightText: 2023 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Console script for pycode128."""

import inspect
import types
from typing import Any, Callable, TypeVar, cast

from click import Choice, echo, version_option
from cloup import HelpFormatter, HelpTheme, Style, argument, command, option, option_group
from cloup.constraints import mutually_exclusive
from python_active_versions.utility import configure_logger

from pycode128 import __version__
from pycode128.code128_image import Code128Image
from pycode128.pycode128 import PyCode128  # pylint: disable=ungrouped-imports   # pylint: disable=no-name-in-module

F = TypeVar('F', bound=Callable[..., Any])


CONTEXT_SETTINGS = {"help_option_names": ['-h', '--help']}

formatter_settings = HelpFormatter.settings(
    theme=HelpTheme(
        invoked_command=Style(fg='bright_yellow'),
        heading=Style(fg='bright_white', bold=True),
        constraint=Style(fg='magenta'),
        col1=Style(fg='bright_yellow'),
    )
)


@command(context_settings=CONTEXT_SETTINGS, show_constraints=True, formatter_settings=formatter_settings)
@argument('data', help='input string to be converted as Code128 label')
@option("-i", "--image", "image_name", type=str, required=False, help="Output file name for generated image.")
@option_group(
    "Format Options",
    option("-c", "--carriage-return", "add_cr", is_flag=True, type=bool, required=False, help="Add ending CR."),
    option(
        "-r",
        "--reader-programming",
        "label_prog",
        is_flag=True,
        type=bool,
        required=False,
        help="Convert to Label Programming Barcode.",
    ),
    option(
        "-a",
        "--action-label",
        "action_label",
        is_flag=True,
        type=bool,
        required=False,
        help="Convert to Action Label Barcode.",
    ),
    constraint=mutually_exclusive,
)
@option_group(
    "Generic Options",
    option(
        '-l',
        '--loglevel',
        'loglevel',
        type=Choice(["debug", "info", "warning", "error"], case_sensitive=False),
        default="info",
        show_default=True,
        help="set log level",
    ),
)
@version_option(__version__)
def pycode128(
    data: str, image_name: str, add_cr: bool, label_prog: bool, action_label: bool, loglevel: str
):  # pylint: disable=R0913
    """Code128 barcode generator library."""
    _fnc_name = cast(types.FrameType, inspect.currentframe()).f_code.co_name
    _complete_doc = inspect.getdoc(eval(_fnc_name))  # pylint: disable=eval-used  # nosec B307
    _doc = f"{_complete_doc}".split('\n')[0]  # use only doc first row
    _str = f"{_doc[:-1]} - v{__version__}"
    echo(f"{_str}")
    echo("=" * len(_str))

    configure_logger(loglevel)

    if add_cr:
        data = f"{data}\r"
    if label_prog:
        data = f"[FNC3] ${data}\r"
    if action_label:
        data = f"[FNC3] {data}\r"
    _code128 = PyCode128(data)
    _code128.encode_raw()
    echo(f"Input string: {data}")
    echo(f"Barcode length: {_code128.length}")
    echo(f"Encoded data: {_code128.encoded_data}")

    if image_name:
        echo(f"Saving image to file: {image_name}")
        Code128Image(_code128.encoded_data).get_image().save(image_name)


if __name__ == "__main__":
    pycode128()  # pragma: no cover  # pylint: disable=no-value-for-parameter
