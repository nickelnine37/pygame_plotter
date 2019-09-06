from typing import Union
import re
import pygame

import numpy as np
import matplotlib.colors as mpl_colors
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm

colors = {**mpl_colors.CSS4_COLORS, **mpl_colors.TABLEAU_COLORS}


def hex_to_RGB(hex_code: str) -> list:
    """
    Convert a hex color code into an RGB triplet

    Parameters
    ----------
    hex_code    A string specifying a hex color code

    Returns
    -------

    RGB         A 3-element RGB vector

    """

    hex_code = hex_code.lstrip('#')
    return [int(hex_code[i:i + 2], 16) for i in (0, 2, 4)]


def is_valid_hex(hex_code: str) -> bool:
    """
    Determine whether a string is a valid hex color code

    Parameters
    ----------
    hex_code    A string

    Returns
    -------
    True is hex_code is a valid hex color code. Else False

    """

    match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_code)

    if match:
        return True
    else:
        return False


def prepare_color(color: Union[str, tuple], alpha=1) -> pygame.Color:
    """
    Convert a color, which could be in any form, into a usuable RGB tuple

    Parameters
    ----------
    color       A color in any form

    Returns
    -------
    RGB         A (r, g, b, a) tuple
    """

    alpha = int(255 * alpha)

    if isinstance(color, str):

        # if it is a simple hex color code, convert to RGB and return
        if is_valid_hex(color):
            return pygame.Color(*tuple(hex_to_RGB(color) + [alpha]))

        # if it is a preset matplotlib color, return the RGB code associated
        elif color in colors:
            return pygame.Color(*tuple(hex_to_RGB(colors[color]) + [alpha]))

        else:
            raise ValueError('{} is not a valid color'.format(color))

    elif isinstance(color, tuple):

        # RGB tuple - add alpha
        if len(color) == 3:
            return pygame.Color(*tuple(list(color) + [alpha]))

        # nothing to do
        elif len(color) == 4:
            return pygame.Color(*color)

        else:
            raise ValueError('Invalid color tuple. Must be RGB(A) but has length {}'.format(len(color)))

    elif isinstance(color, pygame.Color):
        return color

    else:
        raise ValueError('color must be a string, tuple or pygame color')


def color_mapper(cmap: str, vmin: float=0, vmax: float=1, alpha: float=1):
    """
    Return a function that maps floats between vmin and vmax based on a chosen
    color map

    Parameters
    ----------
    cmap        A valid matplotlib color map string
    vmin        The minimum float value
    vmax        The maximum float value
    alpha       Alpha

    Returns
    -------
    A function that takes a single value and outputs a color

    """

    alpha = int(255 * alpha)

    cmap = plt.get_cmap(cmap)
    cNorm = Normalize(vmin=vmin, vmax=vmax)
    scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cmap)

    def mapper(value):
        """
        This is the function that gets returned

        Parameters
        ----------
        value       A number between vmin and vmax

        Returns
        -------
        An RGB color

        """

        out = scalarMap.to_rgba(value)

        if isinstance(out, tuple):
            return tuple([255 * out[i] for i in range(3)] + [alpha])

        elif isinstance(out, np.ndarray):
            out[:, :-1] *= 255
            out[:, 3] = alpha
            return out

    return mapper




