# Copyright 2024-2025 Open Quantum Design

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pydantic import BaseModel, Field
import time

from oqd_teaching_demo.control.trap import Trap
from oqd_teaching_demo.control.lasers import BlueLaser, RedLasers

import threading


class Device(BaseModel):
    trap: Trap = Field(default_factory=Trap)
    red_lasers: RedLasers = Field(default_factory=RedLasers)
    blue_laser: BlueLaser = Field(default_factory=BlueLaser)

    def model_post_init(self, _context=None):
        self._stop_event = threading.Event()

    def stop(self):
        print("Stopping task...")
        self._stop_event.set()

    def run(self, program: Program):
        for i in range(len(program)):
            if self._stop_event.is_set():
                print("Program interrupted.")
                break
            self.red_lasers.set_intensities(intensities=program.red_lasers_intensity[i])

            time.sleep(program.dt)

        self.red_lasers.off()
        return


if __name__ == "__main__":
    n = 10
    red_lasers_intensity = list(
        zip([0, 0.5, 0.75, 0.9, 1.0] * (n // 5), [0, 0.5, 0.75, 0.9, 1.0] * (n // 5))
    )

    print(red_lasers_intensity)
    program = Program(
        camera_trigger=(n - 1) * [0] + [1],
        red_lasers_intensity=list(
            zip(
                [0, 0.5, 0.75, 0.9, 1.0] * (n // 5), [0, 0.5, 0.75, 0.9, 1.0] * (n // 5)
            )
        ),
        phonon_com=n * [1],
        dt=0.2,
    )
    print(len(program.red_lasers_intensity))
    device = Device()
    device.trap.stop()
    device.run(program=program)


