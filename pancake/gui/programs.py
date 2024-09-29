import sys
sys.path.append("/home/oqd/outreach/")

from pancake.program import Program



def program_test():
    n = 10
    red_lasers_intensity = list(zip(
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5)
    ))

    return Program(
        camera_trigger = n * [0],
        red_lasers_intensity = list(zip(
            [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
            [0, 0.5, 0.75, 0.9, 1.0] * (n//5)
        )),
        phonon_com = n * [1],
        dt = 0.2
    )


programs = {
    'test': program_test(),
}
