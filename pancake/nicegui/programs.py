import time
import numpy as np

from pancake.program import Program


def digital_simple():
    n = 10

    red_lasers_intensity = list(zip(
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
    ))

    program = Program(
        camera_trigger = (n-1) * [0] + [1],
        red_lasers_intensity = red_lasers_intensity,
        phonon_com = n * [1],
        dt = 0.2
    )
    return program