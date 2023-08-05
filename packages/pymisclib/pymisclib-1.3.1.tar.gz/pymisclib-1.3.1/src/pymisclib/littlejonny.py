#!/usr/bin/env python3
# vim: fileencoding=utf8
# SPDXVersion: SPDX-2.3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © Copyright 2022, 2023 by Christian Dönges
# SPDXID: SPDXRef-littlejonny-py
"""Format output to a text table.

   In case you have been wondering, the name is a reference to
   https://xkcd.com/327/.
"""
import enum
from argparse import Namespace
from dataclasses import dataclass, field
from typing import Any


# Dictionary of select Unicode characters, keyed by name.
UNICODE_CHARACTERS = {
    # Unicode Box Drawing
    # Range: U+2500—U+257F
    'BOX DRAWINGS LIGHT HORIZONTAL': '─',  # U+2500
    'BOX DRAWINGS HEAVY HORIZONTAL': '━',  # U+2501
    'BOX DRAWINGS LIGHT VERTICAL': '│',  # U+2502
    'BOX DRAWINGS HEAVY VERTICAL': '┃',  # U+2503
    'BOX DRAWINGS LIGHT TRIPLE DASH HORIZONTAL': '┄',  # U+2504
    'BOX DRAWINGS HEAVY TRIPLE DASH HORIZONTAL': '┅',  # U+2505
    'BOX DRAWINGS LIGHT TRIPLE DASH VERTICAL': '┆',  # U+2506
    'BOX DRAWINGS HEAVY TRIPLE DASH VERTICAL': '┇',  # U+2507
    'BOX DRAWINGS LIGHT QUADRUPLE DASH HORIZONTAL': '┈',  # U+2508
    'BOX DRAWINGS HEAVY QUADRUPLE DASH HORIZONTAL': '┉',  # U+2509
    'BOX DRAWINGS LIGHT QUADRUPLE DASH VERTICAL': '┊',  # U+250A
    'BOX DRAWINGS HEAVY QUADRUPLE DASH VERTICAL': '┋',  # U+250B
    'BOX DRAWINGS LIGHT DOWN AND RIGHT': '┌',  # U+250C
    'BOX DRAWINGS DOWN LIGHT AND RIGHT HEAVY': '┍',  # U+250D
    'BOX DRAWINGS DOWN HEAVY AND RIGHT LIGHT': '┎',  # U+250E
    'BOX DRAWINGS HEAVY DOWN AND RIGHT': '┏',  # U+250F
    'BOX DRAWINGS LIGHT DOWN AND LEFT': '┐',  # U+2510
    'BOX DRAWINGS DOWN LIGHT AND LEFT HEAVY': '┑',  # U+2511
    'BOX DRAWINGS DOWN HEAVY AND LEFT LIGHT': '┒',  # U+2512
    'BOX DRAWINGS HEAVY DOWN AND LEFT': '┓',  # U+2513
    'BOX DRAWINGS LIGHT UP AND RIGHT': '└',  # U+2514
    'BOX DRAWINGS UP LIGHT AND RIGHT HEAVY': '┕',  # U+2515
    'BOX DRAWINGS UP HEAVY AND RIGHT LIGHT': '┖',  # U+2516
    'BOX DRAWINGS HEAVY UP AND RIGHT': '┗',  # U+2517
    'BOX DRAWINGS LIGHT UP AND LEFT': '┘',  # U+2518
    'BOX DRAWINGS UP LIGHT AND LEFT HEAVY': '┙',  # U+2519
    'BOX DRAWINGS UP HEAVY AND LEFT LIGHT': '┚',  # U+251A
    'BOX DRAWINGS HEAVY UP AND LEFT': '┛',  # U+251B
    'BOX DRAWINGS LIGHT VERTICAL AND RIGHT': '├',  # U+251C
    'BOX DRAWINGS VERTICAL LIGHT AND RIGHT HEAVY': '┝',  # U+251D
    'BOX DRAWINGS UP HEAVY AND RIGHT DOWN LIGHT': '┞',  # U+251E
    'BOX DRAWINGS DOWN HEAVY AND RIGHT UP LIGHT': '┟',  # U+251F
    'BOX DRAWINGS VERTICAL HEAVY AND RIGHT LIGHT': '┠',  # U+2520
    'BOX DRAWINGS DOWN LIGHT AND RIGHT UP HEAVY': '┡',  # U+2521
    'BOX DRAWINGS UP LIGHT AND RIGHT DOWN HEAVY': '┢',  # U+2522
    'BOX DRAWINGS HEAVY VERTICAL AND RIGHT': '┣',  # U+2523
    'BOX DRAWINGS LIGHT VERTICAL AND LEFT': '┤',  # U+2524
    'BOX DRAWINGS VERTICAL LIGHT AND LEFT HEAVY': '┥',  # U+2525
    'BOX DRAWINGS UP HEAVY AND LEFT DOWN LIGHT': '┦',  # U+2526
    'BOX DRAWINGS DOWN HEAVY AND LEFT UP LIGHT': '┧',  # U+2527
    'BOX DRAWINGS VERTICAL HEAVY AND LEFT LIGHT': '┨',  # U+2528
    'BOX DRAWINGS DOWN LIGHT AND LEFT UP HEAVY': '┩',  # U+2529
    'BOX DRAWINGS UP LIGHT AND LEFT DOWN HEAVY': '┪',  # U+252A
    'BOX DRAWINGS HEAVY VERTICAL AND LEFT': '┫',  # U+252B
    'BOX DRAWINGS LIGHT DOWN AND HORIZONTAL': '┬',  # U+252C
    'BOX DRAWINGS LEFT HEAVY AND RIGHT DOWN LIGHT': '┭',  # U+252D
    'BOX DRAWINGS RIGHT HEAVY AND LEFT DOWN LIGHT': '┮',  # U+252E
    'BOX DRAWINGS DOWN LIGHT AND HORIZONTAL HEAVY': '┯',  # U+252F
    'BOX DRAWINGS DOWN HEAVY AND HORIZONTAL LIGHT': '┰',  # U+2530
    'BOX DRAWINGS RIGHT LIGHT AND LEFT DOWN HEAVY': '┱',  # U+2531
    'BOX DRAWINGS LEFT LIGHT AND RIGHT DOWN HEAVY': '┲',  # U+2532
    'BOX DRAWINGS HEAVY DOWN AND HORIZONTAL': '┳',  # U+2533
    'BOX DRAWINGS LIGHT UP AND HORIZONTAL': '┴',  # U+2534
    'BOX DRAWINGS LEFT HEAVY AND RIGHT UP LIGHT': '┵',  # U+2535
    'BOX DRAWINGS RIGHT HEAVY AND LEFT UP LIGHT': '┶',  # U+2536
    'BOX DRAWINGS UP LIGHT AND HORIZONTAL HEAVY': '┷',  # U+2537
    'BOX DRAWINGS UP HEAVY AND HORIZONTAL LIGHT': '┸',  # U+2538
    'BOX DRAWINGS RIGHT LIGHT AND LEFT UP HEAVY': '┹',  # U+2539
    'BOX DRAWINGS LEFT LIGHT AND RIGHT UP HEAVY': '┺',  # U+253A
    'BOX DRAWINGS HEAVY UP AND HORIZONTAL': '┻',  # U+253B
    'BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL': '┼',  # U+253C
    'BOX DRAWINGS LEFT HEAVY AND RIGHT VERTICAL LIGHT': '┽',  # U+253D
    'BOX DRAWINGS RIGHT HEAVY AND LEFT VERTICAL LIGHT': '┾',  # U+253E
    'BOX DRAWINGS VERTICAL LIGHT AND HORIZONTAL HEAVY': '┿',  # U+253F
    'BOX DRAWINGS UP HEAVY AND DOWN HORIZONTAL LIGHT': '╀',  # U+2540
    'BOX DRAWINGS DOWN HEAVY AND UP HORIZONTAL LIGHT': '╁',  # U+2541
    'BOX DRAWINGS VERTICAL HEAVY AND HORIZONTAL LIGHT': '╂',  # U+2542
    'BOX DRAWINGS LEFT UP HEAVY AND RIGHT DOWN LIGHT': '╃',  # U+2543
    'BOX DRAWINGS RIGHT UP HEAVY AND LEFT DOWN LIGHT': '╄',  # U+2544
    'BOX DRAWINGS LEFT DOWN HEAVY AND RIGHT UP LIGHT': '╅',  # U+2545
    'BOX DRAWINGS RIGHT DOWN HEAVY AND LEFT UP LIGHT': '╆',  # U+2546
    'BOX DRAWINGS DOWN LIGHT AND UP HORIZONTAL HEAVY': '╇',  # U+2547
    'BOX DRAWINGS UP LIGHT AND DOWN HORIZONTAL HEAVY': '╈',  # U+2548
    'BOX DRAWINGS RIGHT LIGHT AND LEFT VERTICAL HEAVY': '╉',  # U+2549
    'BOX DRAWINGS LEFT LIGHT AND RIGHT VERTICAL HEAVY': '╊',  # U+254A
    'BOX DRAWINGS HEAVY VERTICAL AND HORIZONTAL': '╋',  # U+254B
    'BOX DRAWINGS LIGHT DOUBLE DASH HORIZONTAL': '╌',  # U+254C
    'BOX DRAWINGS HEAVY DOUBLE DASH HORIZONTAL': '╍',  # U+254D
    'BOX DRAWINGS LIGHT DOUBLE DASH VERTICAL': '╎',  # U+254E
    'BOX DRAWINGS HEAVY DOUBLE DASH VERTICAL': '╏',  # U+254F
    'BOX DRAWINGS DOUBLE HORIZONTAL': '═',  # U+2550
    'BOX DRAWINGS DOUBLE VERTICAL': '║',  # U+2551
    'BOX DRAWINGS DOWN SINGLE AND RIGHT DOUBLE': '╒',  # U+2552
    'BOX DRAWINGS DOWN DOUBLE AND RIGHT SINGLE': '╓',  # U+2553
    'BOX DRAWINGS DOUBLE DOWN AND RIGHT': '╔',  # U+2554
    'BOX DRAWINGS DOWN SINGLE AND LEFT DOUBLE': '╕',  # U+2555
    'BOX DRAWINGS DOWN DOUBLE AND LEFT SINGLE': '╖',  # U+2556
    'BOX DRAWINGS DOUBLE DOWN AND LEFT': '╗',  # U+2557
    'BOX DRAWINGS UP SINGLE AND RIGHT DOUBLE': '╘',  # U+2558
    'BOX DRAWINGS UP DOUBLE AND RIGHT SINGLE': '╙',  # U+2559
    'BOX DRAWINGS DOUBLE UP AND RIGHT': '╚',  # U+255A
    'BOX DRAWINGS UP SINGLE AND LEFT DOUBLE': '╛',  # U+255B
    'BOX DRAWINGS UP DOUBLE AND LEFT SINGLE': '╜',  # U+255C
    'BOX DRAWINGS DOUBLE UP AND LEFT': '╝',  # U+255D
    'BOX DRAWINGS VERTICAL SINGLE AND RIGHT DOUBLE': '╞',  # U+255E
    'BOX DRAWINGS VERTICAL DOUBLE AND RIGHT SINGLE': '╟',  # U+255F
    'BOX DRAWINGS DOUBLE VERTICAL AND RIGHT': '╠',  # U+2560
    'BOX DRAWINGS VERTICAL SINGLE AND LEFT DOUBLE': '╡',  # U+2561
    'BOX DRAWINGS VERTICAL DOUBLE AND LEFT SINGLE': '╢',  # U+2562
    'BOX DRAWINGS DOUBLE VERTICAL AND LEFT': '╣',  # U+2563
    'BOX DRAWINGS DOWN SINGLE AND HORIZONTAL DOUBLE': '╤',  # U+2564
    'BOX DRAWINGS DOWN DOUBLE AND HORIZONTAL SINGLE': '╥',  # U+2565
    'BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL': '╦',  # U+2566
    'BOX DRAWINGS UP SINGLE AND HORIZONTAL DOUBLE': '╧',  # U+2567
    'BOX DRAWINGS UP DOUBLE AND HORIZONTAL SINGLE': '╨',  # U+2568
    'BOX DRAWINGS DOUBLE UP AND HORIZONTAL': '╩',  # U+2569
    'BOX DRAWINGS VERTICAL SINGLE AND HORIZONTAL DOUBLE': '╪',  # U+256A
    'BOX DRAWINGS VERTICAL DOUBLE AND HORIZONTAL SINGLE': '╫',  # U+256B
    'BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL': '╬',  # U+256C
    'BOX DRAWINGS LIGHT ARC DOWN AND RIGHT': '╭',  # U+256D
    'BOX DRAWINGS LIGHT ARC DOWN AND LEFT': '╮',  # U+256E
    'BOX DRAWINGS LIGHT ARC UP AND LEFT': '╯',  # U+256F
    'BOX DRAWINGS LIGHT ARC UP AND RIGHT': '╰',  # U+2570
    'BOX DRAWINGS LIGHT DIAGONAL UPPER RIGHT TO LOWER LEFT': '╱',  # U+2571
    'BOX DRAWINGS LIGHT DIAGONAL UPPER LEFT TO LOWER RIGHT': '╲',  # U+2572
    'BOX DRAWINGS LIGHT DIAGONAL CROSS': '╳',  # U+2573
    'BOX DRAWINGS LIGHT LEFT': '╴',  # U+2574
    'BOX DRAWINGS LIGHT UP': '╵',  # U+2575
    'BOX DRAWINGS LIGHT RIGHT': '╶',  # U+2576
    'BOX DRAWINGS LIGHT DOWN': '╷',  # U+2577
    'BOX DRAWINGS HEAVY LEFT': '╸',  # U+2578
    'BOX DRAWINGS HEAVY UP': '╹',  # U+2579
    'BOX DRAWINGS HEAVY RIGHT': '╺',  # U+257A
    'BOX DRAWINGS HEAVY DOWN': '╻',  # U+257B
    'BOX DRAWINGS LIGHT LEFT AND HEAVY RIGHT': '╼',  # U+257C
    'BOX DRAWINGS LIGHT UP AND HEAVY DOWN': '╽',  # U+257D
    'BOX DRAWINGS HEAVY LEFT AND LIGHT RIGHT': '╾',  # U+257E
    'BOX DRAWINGS HEAVY UP AND LIGHT DOWN': '╿',  # U+257F
}  # UNICODE_CHARACTERS


# Box drawing characters.
# The beauty of Namespace makes it possible to access a character like so:
# box_drawings.light.horizontal.
box_drawings = Namespace(
    double=Namespace(
        down_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE DOWN AND HORIZONTAL'],
        down_and_left=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE DOWN AND LEFT'],
        down_and_right=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE DOWN AND RIGHT'],
        horizontal=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE HORIZONTAL'],
        up_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE UP AND HORIZONTAL'],
        up_and_left=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE UP AND LEFT'],
        up_and_right=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE UP AND RIGHT'],
        vertical=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE VERTICAL'],
        vertical_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE VERTICAL AND HORIZONTAL'],
        vertical_and_left=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE VERTICAL AND LEFT'],
        vertical_and_right=UNICODE_CHARACTERS['BOX DRAWINGS DOUBLE VERTICAL AND RIGHT'],
    ),  # double
    light=Namespace(
        down_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT DOWN AND HORIZONTAL'],
        down_and_left=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT DOWN AND LEFT'],
        down_and_right=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT DOWN AND RIGHT'],
        horizontal=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT HORIZONTAL'],
        up_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT UP AND HORIZONTAL'],
        up_and_left=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT UP AND LEFT'],
        up_and_right=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT UP AND RIGHT'],
        vertical=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT VERTICAL'],
        vertical_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT VERTICAL AND HORIZONTAL'],
        vertical_and_left=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT VERTICAL AND LEFT'],
        vertical_and_right=UNICODE_CHARACTERS['BOX DRAWINGS LIGHT VERTICAL AND RIGHT'],
    ),  # light
    heavy=Namespace(
        down_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY DOWN AND HORIZONTAL'],
        down_and_left=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY DOWN AND LEFT'],
        down_and_right=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY DOWN AND RIGHT'],
        horizontal=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY HORIZONTAL'],
        up_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY UP AND HORIZONTAL'],
        up_and_left=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY UP AND LEFT'],
        up_and_right=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY UP AND RIGHT'],
        vertical=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY VERTICAL'],
        vertical_and_horizontal=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY VERTICAL AND HORIZONTAL'],
        vertical_and_left=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY VERTICAL AND LEFT'],
        vertical_and_right=UNICODE_CHARACTERS['BOX DRAWINGS HEAVY VERTICAL AND RIGHT'],
    )  # heavy
)  # box_drawings


@enum.unique
class LineStyle(enum.Enum):
    """Rendering style for lines."""
    double = box_drawings.double
    light = box_drawings.light
    heavy = box_drawings.heavy


Text = list[str]


@dataclass
class ColumnTable:
    """Table with data arranged by column."""
    _headings: list[str] = field(default_factory=list)  # row or column heading
    _formats: list[str] = field(default_factory=list)  # cell formats
    _cells: list[list[Any]] = field(default_factory=list)  # column[row]
    _num_columns: int = 0
    _num_rows: int = 0

    @property
    def cell_formats(self) -> list[str]:
        """Return headings."""
        return self._formats

    @property
    def headings(self) -> list[str]:
        """Return headings."""
        return self._headings

    @property
    def num_columns(self):
        return self._num_columns

    @property
    def num_rows(self):
        return self._num_rows

    def set_table(self,
                  headings: list[str],
                  cell_formats: list[str],
                  cells: list[list[str]]):
        """Set the headings, the format of the cells, and the cell content.

           The cells are specified column[row].
        """
        if len(headings) != len(cell_formats):
            raise ValueError('number columns in headings and formats do not match')
        if len(headings) != len(cells):
            raise ValueError('number of columns in headings and cells do not match')
        self._num_columns = len(headings)
        self._num_rows = len(cells[0])
        self._headings = headings
        self._formats = cell_formats
        self._cells = cells

    def set_table_transposed(self,
                             headings: list[str],
                             cell_formats: list[str],
                             cells: list[list[str]]):
        """The cells are specified row[column]."""
        transposed_cells = [list(x) for x in zip(*cells)]
        self.set_table(headings, cell_formats, transposed_cells)

    def draw(self, style: LineStyle) -> Text:
        """Draw the table to a list of lines."""
        formatted_cells = []
        column_widths = []
        for c in range(self.num_columns):
            column_width = len(self._headings[c])
            column_data = self._cells[c]
            fmt = self._formats[c]
            formatted_column = []
            for cell in column_data:
                formatted_cell = f'{cell:{fmt}}'
                formatted_column.append(formatted_cell)
                column_width = max(column_width,  len(formatted_cell))
            formatted_cells.append(formatted_column)
            column_widths.append(column_width)

        box = style.value
        lines = []
        first = True
        s = ''
        for c in range(self.num_columns):
            column_width = column_widths[c]
            if first:
                s = box.down_and_right + box.horizontal * (column_width + 2)
                first = False
            else:
                s += box.down_and_horizontal + box.horizontal * (column_width + 2)
        s += box.down_and_left
        lines.append(s)

        s = ''
        for c in range(self.num_columns):
            column_width = column_widths[c]
            s += box.vertical + f' {self._headings[c]:{column_width}s} '
        s += box.vertical
        lines.append(s)

        first = True
        s = ''
        for c in range(self.num_columns):
            column_width = column_widths[c]
            if first:
                s = box.vertical_and_right + box.horizontal * (column_width + 2)
                first = False
            else:
                s += box.vertical_and_horizontal + box.horizontal * (column_width + 2)
        s += box.vertical_and_left
        lines.append(s)

        for r in range(self.num_rows):
            s = ''
            for c in range(self.num_columns):
                column_width = column_widths[c]
                s += box.vertical + f' {formatted_cells[c][r]:{column_width}s} '
            s += box.vertical
            lines.append(s)

        first = True
        s = ''
        for c in range(self.num_columns):
            column_width = column_widths[c]
            if first:
                s = box.up_and_right + box.horizontal * (column_width + 2)
                first = False
            else:
                s += box.up_and_horizontal + box.horizontal * (column_width + 2)
        s += box.up_and_left
        lines.append(s)

        return lines


def draw_box(x, y, style) -> Text:
    """Construct a box of size x * y with style."""
    box = style.value

    lines = []
    s = box.down_and_right + box.horizontal * x + box.down_and_left
    lines.append(s)
    s = box.vertical + ' ' * x + box.vertical
    for i in range(y):
        lines.append(s)
    s = box.up_and_right + box.horizontal * x + box.up_and_left
    lines.append(s)

    return lines


def print_lines(lines: Text):
    """Print lines stored as a list of strings to stdout."""
    for line in lines:
        print(line)


if __name__ == '__main__':
    print_lines(draw_box(5, 3, LineStyle.light))
    print_lines(draw_box(1, 1, LineStyle.double))
    print_lines(draw_box(40, 3, LineStyle.heavy))

    ct1 = ColumnTable()
    ct1.set_table_transposed(
        headings=['First', 'Second', 'Third', 'Fourth'],
        cell_formats=['3d', '08x', 's', '>s'],
        cells=[[1, 0x12345678, 'abc def geh', 'this is a sample text'],
               [2, 0xffffee01, '12345', 'Short'],
               [12, -1, 'minus one', 'negative hex number'],
               [123, 0, 'zero', 'Zero hexadecimal number'],
               [1000, 23, 'First', 'The first column is too large.']]
    )
    print_lines(ct1.draw(LineStyle.light))
