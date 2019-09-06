import pygame
import sys
import numpy as np

from .screen import Screen

clock = pygame.time.Clock()
screen = Screen(xlim=(-5, 5), ylim=(-5, 5))
x = np.linspace(-3, 3, 101)

t = 0

while True:

    screen.plot(np.array([-3, 3]), np.array([0, 0]))
    screen.plot(np.array([0, 0]), np.array([-3, 3]))

    screen.plot(x, np.sin(3 *( x - t)))
    screen.update()

    clock.tick(30)
    t += 1 / 30