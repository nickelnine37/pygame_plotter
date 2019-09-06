import pygame
from typing import Union
from pygame import gfxdraw
import numpy as np
import sys

from .color import prepare_color

class Screen:

    """
    Screen class. This
    """

    def __init__(self, size: tuple=(1920, 1080), xlim: tuple=(0, 1), ylim: tuple=(0, 1), background='black'):
        """
        Initialise a Screen object

        Parameters
        ----------
        size          Screen size in pixels (length, height)
        xlim          The x-limits. (left, right)
        ylim          The y-limits. (bottom, top)
        screen_color  The screen color
        """

        self.canvas = pygame.display.set_mode(size)
        self.background = prepare_color(background)
        self.canvas.fill(self.background)

        self.size = self.canvas.get_size()
        self.xlim = np.array(xlim).astype(float)
        self.ylim = np.array(ylim).astype(float)

        self.CLICKED = False
        self.last_mouse_position = None
        self.DRAW_MODE = False
        self.raw_lines = []
        self.interpolated_lines = []
        self.current_line = []
        self.n_lines = 0

    def draw_cricle(self, pos: tuple, color: Union[str, tuple]=(255, 255, 255), radius: int=5):

        if isinstance(color, str):
            color = pygame.Color(color)

        # pygame.draw.circle(self.canvas, color, self.xy_to_pix(pos), radius)
        pygame.gfxdraw.filled_circle(self.canvas, *self.xy_to_pix(pos), radius, color)

    def xy_to_pix(self, pos: tuple):

        px = int(np.round(self.size[0] * (pos[0] - self.xlim[0]) / (self.xlim[1] - self.xlim[0]), 0))
        py = int(np.round(self.size[1] * (self.ylim[1] - pos[1]) / (self.ylim[1] - self.ylim[0]), 0))

        return px, py

    def pix_to_xy(self, pos: tuple):

        x = self.xlim[1] + (self.xlim[0] - self.xlim[1]) * (1 - pos[0] / self.size[0])
        y = self.ylim[0] + (self.ylim[1] - self.ylim[0]) * (1 - pos[1] / self.size[1])

        return x, y

    def xy_array_to_pix(self, pos: np.ndarray):

        px = np.round(self.size[0] * (pos[0, :] - self.xlim[0]) / (self.xlim[1] - self.xlim[0]), 0).astype(int)
        py = np.round(self.size[1] * (self.ylim[1] - pos[1, :]) / (self.ylim[1] - self.ylim[0]), 0).astype(int)

        return np.array([px, py]).T

    def plot(self, x: np.ndarray, y: np.ndarray, color: Union[str, tuple, pygame.Color]=(255, 255, 255), width: int=1):
        """
        Plot a curve, similar to pyplot.plot

        Parameters
        ----------
        x       numpy array (n, ) holding x values to plot at
        y       numpy array (n, ) holding y values to plot
        color   the line color
        width   the line width in pixels

        """

        pygame.draw.lines(self.canvas, prepare_color(color), False, self.xy_array_to_pix(np.array([x, y])), width)

    def get_mouse_position(self):
        return self.pix_to_xy(pygame.mouse.get_pos())

    def handle_zooming(self, event):
        """
        Handle zooming, triggered by a mouse roll

        Parameters
        ----------
        event       The zoom event

        """

        # the zoom factor
        zoom = 0.05

        # zoom in
        if event.button == 4:
            self.ylim = (1 - zoom) * self.ylim + zoom * (self.ylim[1] + self.ylim[0]) / 2
            self.xlim = (1 - zoom) * self.xlim + zoom * (self.xlim[1] + self.xlim[0]) / 2

        # zoom out
        if event.button == 5:
            self.ylim = (1 + zoom) * self.ylim - zoom * (self.ylim[1] + self.ylim[0]) / 2
            self.xlim = (1 + zoom) * self.xlim - zoom * (self.xlim[1] + self.xlim[0]) / 2

    def handle_panning(self):
        """
        Handle panning, triggered by dragging the mouse

        """

        if self.CLICKED:
            pos_change = self.last_mouse_position - np.array(self.get_mouse_position())
            self.xlim += pos_change[0]
            self.ylim += pos_change[1]

        self.last_mouse_position = np.array(self.get_mouse_position())

    def handle_drawing(self):

        if self.CLICKED:
            self.current_line.append(self.get_mouse_position())
            if len(self.raw_lines) > self.n_lines:
                del self.raw_lines[-1]
            self.raw_lines.append(np.array(self.current_line))

        self.last_mouse_position = np.array(self.get_mouse_position())

    def update(self):


        for event in pygame.event.get():

            # if we exit
            if event.type == pygame.QUIT:
                sys.exit()

            # handle zooming
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_zooming(event)

            if event.type == pygame.KEYDOWN:

                # enter draw mode
                if event.key == 100:
                    if not self.DRAW_MODE:
                        self.DRAW_MODE = True
                    else:
                        self.DRAW_MODE = False

        # handle panning
        if pygame.mouse.get_pressed()[0]:
            if not self.DRAW_MODE:
                self.handle_panning()
            else:
                self.handle_drawing()
            self.CLICKED = True

        else:
            if self.CLICKED:
                if self.DRAW_MODE:
                    self.current_line = []
                    self.n_lines += 1
            self.CLICKED = False


        pressed_keys = np.argwhere(pygame.key.get_pressed())

        # if we hit ctrl+z, remove last line
        if 122 in pressed_keys and 306 in pressed_keys:
            if len(self.raw_lines) > 0:
                del self.raw_lines[-1]

        # quit if we hit esc
        if 27 in pressed_keys:
            sys.exit()

        # draw lines
        for line in self.raw_lines:
            if line.shape[0] > 1:
                self.plot(line[:, 0], line[:, 1])


        pygame.display.update()
        self.canvas.fill(self.background)
