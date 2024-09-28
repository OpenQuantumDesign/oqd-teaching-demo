from pydantic import BaseModel, Field
from pydantic.types import Union

import sys
sys.path.append("/home/oqd/outreach/")

# from pancake.base import TypeReflectBaseModel

from pancake.control.trap import Trap
from pancake.control.lasers import LaserArray, BlueLaser, RedLasers, GreenLaser
# from pancake.control.camera import Camera
from pancake.program import Program

import threading 



class Device(BaseModel):
    trap: Trap = Field(default_factory=Trap)
    red_lasers: RedLasers = Field(default_factory=RedLasers)
    # blue_laser: BlueLaser
    # green_laser: GreenLaser
    # camera: Camera


    def model_post_init(self, _context=None):
        self._stop_event = threading.Event()

    def perform_task(self):
        # Simulate a long-running task with hardware (e.g., controlling lasers)
        import time
        for i in range(10):
            if self._stop_event.is_set():
                print("Task interrupted!")
                break
            print(f"Running task step {i + 1}")
            time.sleep(1)  # Simulate work

    def stop_task(self):
        print("Stopping task...")
        self._stop_event.set()

    def run_program(self, program: Program):
        for i in range(len(program)):
            print(i)
        return

    # def run(self, program: Program):

        # return

    
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

device = Device()
device.run_program(program=program)