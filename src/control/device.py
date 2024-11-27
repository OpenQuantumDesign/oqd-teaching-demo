from pydantic import BaseModel, Field
import time
import sys
sys.path.append("/home/oqd/outreach/")

# from pancake.base import TypeReflectBaseModel

from src import Trap
from src import BlueLaser, RedLasers
# from pancake.control.camera import Camera
from src import Program

import threading 



class Device(BaseModel):
    trap: Trap = Field(default_factory=Trap)
    red_lasers: RedLasers = Field(default_factory=RedLasers)
    blue_laser: BlueLaser = Field(default_factory=BlueLaser)


    def model_post_init(self, _context=None):
        self._stop_event = threading.Event()

    # def perform_task(self):
    #     # Simulate a long-running task with hardware (e.g., controlling lasers)
    #     import time
    #     for i in range(10):
    #         if self._stop_event.is_set():
    #             print("Task interrupted!")
    #             break
    #         print(f"Running task step {i + 1}")
    #         time.sleep(1)  # Simulate work

    def stop(self):
        print("Stopping task...")
        self._stop_event.set()

    def run(self, program: Program):
        for i in range(len(program)):
            if self._stop_event.is_set():
                print("Program interrupted.")
                break
            self.red_lasers.set_intensities(intensities=program.red_lasers_intensity[i])
            # device.trap.set_intensities(intentensities=program.red_lasers_intensities[i])

            # if i > 0: 
            #     if program.camera_trigger[i] - program.camera_trigger[i-1] == +1:  # rising edge
            #         self.camera.capture(file=f"step{i}")

            time.sleep(program.dt)

        self.red_lasers.off()
        return


    

if __name__ == "__main__":
    n = 10
    red_lasers_intensity = list(zip(
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
        [0, 0.5, 0.75, 0.9, 1.0] * (n//5)
    ))

    print(red_lasers_intensity)
    program = Program(
        camera_trigger = (n-1) * [0] + [1],
        red_lasers_intensity = list(zip(
            [0, 0.5, 0.75, 0.9, 1.0] * (n//5),
            [0, 0.5, 0.75, 0.9, 1.0] * (n//5)
        )),
        phonon_com = n * [1],
        dt = 0.2
    )
    print(len(program.red_lasers_intensity))
    device = Device()
    device.trap.stop()
    # device.run(program=program)