import re
from textwrap import fill, wrap

import numpy as np

# def plotTitle(titleStr, linelength=60):
#     """Format a long plot title, nicely wrapping text

#     Args:
#         titleStr (str): the title for the plot
#         linelength (int, optional): Maximum line length for wrapping. Defaults to 60.

#     Returns:
#         str: The title with line breaks
#     """
#     return "\n".join(wrap(titleStr, linelength))


def plotTitle(titleStr, target_line_length=70):
    """Format a long plot title, nicely wrapping text,
    including strings with math blocks ($a = b$) which should not be broken.


    Args:
        titleStr (str): the title for the plot
        target_line_length (int, optional): Targeted (non-strict) line length for wrapping. Defaults to 60.

    Returns:
        str: The title with line breaks
    """

    titleStr = titleStr.strip()

    spaces = [m.start() for m in re.finditer(" ", titleStr)]
    mathblocks_all = [m.start() for m in re.finditer("\$", titleStr)]
    if len(mathblocks_all) > 0:
        mathblocks = []
        for i in range(len(mathblocks_all), 2):
            mathblocks.append((mathblocks_all[i], mathblocks_all[i + 1]))

        for r in mathblocks:
            [spaces.remove(i) for i in range(r[0], r[1]) if i in spaces]

    spaces = np.array(spaces)

    lines = []
    remaining_length = len(titleStr)
    i0 = 0
    while remaining_length > 0:
        if len(titleStr[i0:]) < target_line_length:
            lines.append(titleStr[i0:])
            break
        line_length = target_line_length
        i = spaces[spaces < line_length * (len(lines) + 1)].max()
        lines.append(titleStr[i0:i])
        i0 = i + 1
        remaining_length = len(titleStr[i0:])

    str = ""
    for l in lines:
        str += l + "\n"

    return str[:-1]
