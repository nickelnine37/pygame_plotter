import time
import pygame
import sys
from screen import Screen
from color import color_mapper
import numpy as np

FRAME_RATE = 30
duration = 60


presets = {1: {'t0': -0.42,
               't1': -0.40,
               'x0': -1.03,
               'x1':  0.28,
               'y0': -0.55,
               'y1':  0.40,
               'x_': lambda x, y, t: -y ** 2 - x * t + y,
               'y_': lambda x, y, t: x ** 2 - x * y + t,
               'n_iters': 150,
               'trail_length': 10},

           2: {'t0': 0.0249,
               't1': 0.025,
               'x0': -0.4,
               'x1':  0.65,
               'y0': -0.5,
               'y1':  0.7,
               'x_': lambda x, y, t: -x ** 2 + x * t + y,
               'y_': lambda x, y, t: x ** 2 - y ** 2 - t ** 2 - x * y + y * t -x + y,
               'n_iters': 350,
               'trail_length': 20},

           3: {'t0': 0.400,
               't1': 0.400001,
               'x0': -0.75,
               'x1': 1.7,
               'y0': -1.29,
               'y1': 0.45,
               'x_': lambda x, y, t: x ** 2 + -x * t + y * t - x,
               'y_': lambda x, y, t: - y ** 2 - t ** 2 - x * y - y * t - x * t - y,
               'n_iters': 130,
               'trail_length': 10},

           4: {'t0': 0.021,
               't1': 0.0215,
               'x0': -0.4,
               'x1': 0.6,
               'y0': -0.5,
               'y1': 0.6,
               'x_': lambda x, y, t: -x ** 2 + x * t + y,
               'y_': lambda x, y, t: x ** 2 - y ** 2 - t ** 2 - x * y + y * t - x  + y,
               'n_iters': 400,
               'trail_length': 10},

           5: {'t0': -0.2,
               't1': 0,
               'x0': -1,
               'x1': 1,
               'y0': -1,
               'y1': 1,
               'x_': lambda x, y, t: -x ** 2 + x * t * y + y,
               'y_': lambda x, y, t: x ** 2 - y ** 2 - t ** 2 - x * y + y * t - x + y,
               'n_iters': 350,
               'trail_length': 10},


           6: {'t0': 0.10810076872,
               't1': 0.108100768755,
               'x0': -1.5,
               'x1': 1.3,
               'y0': 0,
               'y1': 2,
               'x_': lambda x, y, t: -t ** 2 - x * y + t,
               'y_': lambda x, y, t: - x * y + x * t + y + t,
               'n_iters': 800,
               'trail_length': 10},

           7: {'t0': -1.189,
               't1': -1.188,
               'x0': -0.8,
               'x1': -0.2,
               'y0': -2,
               'y1': 1,
               'x_': lambda x, y, t: t ** -2 + x ** 2 - t ** 2,
               'y_': lambda x, y, t: - x * y + y ** 2 - t** 2,
               'n_iters': 150,
               'trail_length': 10},

           8: {'t0': -0.75,
               't1': -0.5,
               'x0': -1,
               'x1': 1,
               'y0': -1,
               'y1': 1,
               'x_': lambda x, y, t: t ** 2 - x * y + x * t,
               'y_': lambda x, y, t: y ** 2 - x ** 2 + t ** 2,
               'n_iters': 150,
               'trail_length': 10},

           9: {'t0': 0.195,
               't1': 0.19502,
               'x0': -0.9,
               'x1': -0.5,
               'y0': -0.4,
               'y1': -0.1,
               'x_': lambda x, y, t: t - x * y + x * t - x * 2,
               'y_': lambda x, y, t: y ** 2 - x ** 2 + t ** 2,
               'n_iters': 150,
               'trail_length': 10},

           10: {'t0': -0.788,
                't1': -0.786,
                'x0': -1.8,
                'x1': 0.85,
                'y0': -1.2,
                'y1': 1.8,
                'x_': lambda x, y, t: t - x * y + x * t - x ** 2,
                'y_': lambda x, y, t: t ** 2 - y ** 2 + t * x,
                'n_iters': 350,
                'trail_length': 10},


           11: {'t0': -0.00437,
                't1': -0.00434,
                'x0': -1,
                'x1': 1,
                'y0': -1,
                'y1': 1,
                'x_': lambda x, y, t: y + x + t,
                'y_': lambda x, y, t: y ** 2 - x ** 2 + t - y,
                'n_iters': 500,
                'trail_length': 10},

           12: {'t0': -0.0001,
                't1': 0.035,
                'x0': -2,
                'x1': 0.2,
                'y0': -2,
                'y1': 1.2,
                'x_': lambda x, y, t: t * x + t ** 2 - y ** 2,
                'y_': lambda x, y, t: x ** 2 - t ** 2 + y + x - t,
                'n_iters': 300,
                'trail_length': 10},

           13: {'t0': -0.6,
                't1': -0.37,
                'x0': -1.5,
                'x1': 1.5,
                'y0': -1.5,
                'y1': 1.5,
                'x_': lambda x, y, t: x * t - y * x + y * t - x ** 2 + y ** 2,
                'y_': lambda x, y, t: y ** 2 - t ** 2 + x ** 2 - y * t + x - y,
                'n_iters': 300,
                'trail_length': 10},
}

def load(preset: dict):

    t0, t1 = preset['t0'], preset['t1']
    screen = Screen((1920, 1080), xlim=(preset['x0'], preset['x1']), ylim=(preset['y0'], preset['y1']))
    x_, y_ = preset['x_'], preset['y_']

    return preset['n_iters'], preset['trail_length'], preset['x0'], preset['x1'], preset['y0'], preset['y1'], t0, t1, x_, y_, screen


n_iters, trail_length, x0, x1, y0, y1, t0, t1, x_, y_, screen = load(presets[10])
t = t0

# animation time in seconds
ts = np.linspace(t0, t1, duration * FRAME_RATE)

# real time tracker
T = 0

clock = pygame.time.Clock()

mappers = [color_mapper('hsv', vmin=0, vmax=n_iters, alpha=1 - i / trail_length) for i in range(trail_length)]
colors = [[mappers[i](j) for j in range(n_iters)] for i in range(trail_length)]

def get_coords(t):

    coords = [(t, t)]
    for i in range(n_iters):
        x, y = coords[i]
        try:
            coords.append((x_(x, y, t), y_(x, y, t)))
        except OverflowError:
            break

    return coords[1:]

points_list = []

bits = int(np.ceil(np.log2(2 * len(ts))))


for j, t in enumerate(ts):


    T1 = time.time()
    points_list.append(get_coords(t))

    if len(points_list) > trail_length:
        del points_list[0]

    pl = np.array(points_list)

    for i, points in enumerate(reversed(points_list)):
        for point, color in zip(points, colors[i]):
            if all([point[0] < x1, point[0] > x0, point[1] < y1, point[1] > y0]):
                screen.draw_cricle(point, radius=2, color=color)

    screen.update()





