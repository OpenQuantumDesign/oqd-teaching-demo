from pydantic import BaseModel
from pydantic.types import Union

from pancake.base import TypeReflectBaseModel

from pancake.control.trap import Trap
from pancake.control.lasers import LaserArray, BlueLaser, RedLasers, GreenLaser
# from pancake.control.camera import Camera


# class Program(TypeReflectBaseModel):
# 
    # pass


class Device(BaseModel):
    trap: Trap
    red_lasers: RedLasers
    # blue_laser: BlueLaser
    # green_laser: GreenLaser
    # camera: Camera

    # def run(self, program: Program):

        # return

    

