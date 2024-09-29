from pydantic import BaseModel
from pydantic.types import Union




class Program(BaseModel):
    camera_trigger: list[bool]
    red_lasers_intensity: list[list[float]]
    phonon_com: list[bool]
    dt: float

    # todo: validate the length of all

    def __len__(self):
        return len(self.camera_trigger)


# if __name__ == "__main__":

#     n = 10
#     program = Program(
#         camera_trigger = n * [0],
#         red_lasers_intensity = zip(
#             [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
#             [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
#             [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
#             [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
#             [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
#          ),
#         phonon_com = n * [1],
#         dt = 0.2
#     )

#     print(program)