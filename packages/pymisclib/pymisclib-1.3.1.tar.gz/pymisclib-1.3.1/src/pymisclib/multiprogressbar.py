#!/usr/bin/env python3
# vim: fileencoding=utf8
# SPDXVersion: SPDX-2.3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © Copyright 2012-2022, 2023 by Christian Dönges
# SPDXID: SPDXRef-multiprogressbar-py
"""Print multiple progress bars to the console.

   The configuration of the bars is handled through a list of dictionaries.
   Each dictionary contains the parameters for a single progress bar.

   Before the bars are shown, ``prepare_bars()`` must be called to make room for
   the bars on the console.

   Each time a bar is updated, ``print_bars()`` is called to update the console
   output.

   Bar example
   -----------

   A simple example shows a bar for the entire process and a second bar for
   individual progress steps below the first bar.

   This is an example: ::

       Total |------------------------------| 0% Writing
             |███████████████---------------| 50.9% /tmp3muil9sc/0000000000000000.tmp


   .. code-block:: python

       from multiprogressbar import prepare_bars, print_bars

       config = [
           {
               'current_iteration': 0,
               'total_iterations': 5,
               'prefix': 'Total',
               'suffix': 'Writing',
               'decimals': 0,
               'bar_length': 30},
           {
               'current_iteration': 509,
               'total_iterations': 1000,
               'prefix': '     ',
               'suffix': '/tmp3muil9sc/0000000000000000.tmp',
               'decimals': 1,
               'bar_length': 30},
       ]
       prepare_bars(config)
       print_bars(config)

"""

import enum
import sys
from time import sleep


@enum.unique
class BAR_COLORS(enum.Enum):
    """Colors and the ANSI format strings used to create them."""
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    BrightBlack = '\033[1;30m'
    BrightRed = '\033[1;31m'
    BrightGreen = '\033[1;32m'
    BrightYellow = '\033[1;33m'
    BrightBlue = '\033[1;34m'
    BrightMagenta = '\033[1;35m'
    BrightCyan = '\033[1;36m'
    BrightWhite = '\033[1;37m'


def print_single_bar(
        current_iteration: int,
        total_iterations: int,
        prefix: str = '',
        suffix: str = '',
        decimals: int = 1,
        bar_length: int = 80,
        bar_color: BAR_COLORS = BAR_COLORS.Black):
    """Output a single progress bar to stdout.

    :param int current_iteration: the current iteration
    :param int total_iterations: the total number of iterations
    :param str prefix: a string that will be output before the bar
    :param str suffix: a string that will be output after the bar
    :param int bar_length: the length of the bar in characters
    :param BAR_COLORS bar_color: the color of the bar.

    """
    current_iteration = min(current_iteration, total_iterations)

    percents = f'{100 * (current_iteration / float(total_iterations)):.{decimals}f}'
    filled_length = int(round(bar_length * current_iteration / float(total_iterations)))
    the_bar = f'{"█" * filled_length}{"-" * (bar_length - filled_length)}'

    sys.stdout.write(
        f'\x1b[2K\r{prefix} |{bar_color.value}{the_bar}'
        f'{BAR_COLORS.Black.value}| {percents}% {suffix}')


def prepare_bars(configs: list):
    """Print to prepare for the bars."""
    for c in configs:
        sys.stdout.write('\n')


def print_bars(configs: list):
    """Print progress bars."""
    # Move the cursor up to the start of the line of the first bar.
    for n in range(len(configs)):
        sys.stdout.write('\033[F')  # up

    for config in configs:
        ci = config['current_iteration']
        ti = config['total_iterations']
        prefix = config.get('prefix', '')
        suffix = config.get('suffix', '') + '\033[K\n'
        decimals = config.get('decimals', 1)
        bar_length = config.get('bar_length', 80)
        bar_color = config.get('bar_color', BAR_COLORS.Black)
        print_single_bar(ci, ti, prefix, suffix, decimals, bar_length,
                         bar_color)
    sys.stdout.flush()


def main():
    """Demonstration of how it works."""
    configs = [
        {
            'current_iteration': 0,
            'total_iterations': 5,
            'prefix': 'Total',
            'suffix': 'Writing',
            'decimals': 0,
            'bar_length': 30,
            'bar_color': BAR_COLORS.Green,
        },
        {
            'current_iteration': 509,
            'total_iterations': 1000,
            'prefix': '     ',
            'suffix': '/tmp3muil9sc/0000000000000000.tmp',
            'decimals': 1,
            'bar_length': 30
        },
        {
            'current_iteration': 1,
            'total_iterations': 10,
            'bar_length': 15,
            'bar_color': BAR_COLORS.BrightRed,
        },
        {
            'current_iteration': 0,
            'total_iterations': 100,
            'prefix': 'Jolly'
        },
    ]
    prepare_bars(configs)
    for i in range(100):
        print_bars(configs)
        for config in configs:
            config['current_iteration'] += 1
        sleep(.1)


if __name__ == '__main__':
    main()
