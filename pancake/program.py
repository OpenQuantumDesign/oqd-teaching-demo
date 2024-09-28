from pydantic import BaseModel
from pydantic.types import Union




class Program(BaseModel):
    camera: list[bool]
    lasers: list[list[float]]
    trap: list[bool]
    dt: float

    # todo: validate the length of all

    def __len__(self):
        return len(self.camera)


n = 10
program = Program(
    camera = n * [0],
    lasers = [
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
    ],
    trap = n * [1],
    dt = 0.2
)

print(program)