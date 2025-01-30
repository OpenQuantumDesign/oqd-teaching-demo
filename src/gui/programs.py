import numpy as np

from src import Program


def digital_simple():
    n = 10

    red_lasers_intensity = list(zip(
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
    ))

    program = Program(
        # camera_trigger = (n-1) * [0] + [1],
        red_lasers_intensity = red_lasers_intensity,
        # phonon_com = n * [1],
        dt = 0.2
    )
    return program



def digital_shor():
    repeats = 4
    red_lasers_intensity = list(zip(
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1] * repeats,
        [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1] * repeats,
        [1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1] * repeats,
        [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1] * repeats,
    ))
    program = Program(
        red_lasers_intensity = red_lasers_intensity,
        dt = 0.25
    )
    return program


def digital_random(n: int = 20):
    red_lasers_intensity = list(zip(
        list(np.random.randint(0, 2, n)),
        list(np.random.randint(0, 2, n)),
        list(np.random.randint(0, 2, n)),
        list(np.random.randint(0, 2, n)),
    ))
    program = Program(
        red_lasers_intensity = red_lasers_intensity,
        dt = 0.25
    )
    return program


def analog_ising(n: int = 60):
    t = np.arange(n)
    dt = 0.1
    period = 0.1
    red_lasers_intensity = list(zip(
        list((np.sin(t * dt / period + 0) + 1)/2),
        list((np.sin(t * dt / period + 0)+1)/2),
        list((np.sin(t * dt / period + np.pi/2)+1)/2),
        list((np.sin(t * dt / period + np.pi/2)+1)/2),
    ))
    program = Program(
        red_lasers_intensity = red_lasers_intensity,
        dt = dt
    )
    return program


def analog_all_to_all(n: int = 60):
    t = np.arange(n)
    dt = 0.1
    period = 0.2
    red_lasers_intensity = list(zip(
        list((np.sin(t * dt / period + 0)+1)/2),
        list((np.sin(t * dt / period + 0)+1)/2),
        list((np.sin(t * dt / period + 0)+1)/2),
        list((np.sin(t * dt / period + 0)+1)/2),
    ))
    program = Program(
        red_lasers_intensity = red_lasers_intensity,
        dt = dt
    )
    return program