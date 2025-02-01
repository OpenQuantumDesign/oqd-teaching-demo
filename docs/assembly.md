# Assembly of the demo

1. **Build the acoustic trap**
   1. Source all materials and 3D print components, see [Materials](./materials.md).
   2. Follow the [Instructable](https://www.instructables.com/Acoustic-Levitator/) and the [journal publication](https://doi.org/10.1063/1.4989995) to assemble the acoustic trap apparatus.

2. **3D print the enclosure**
   1. Print all objects provided as STL files in the [`design/objects`](../design/objects/) folder.
   2. Install the on/off switch on the right-hand side of the bottom enclosure, and connect it to a power source.

3. **Connect the lasers, trap, and camera**
   1. Connect the [holder](../design/objects/joint1.stl) and [socket](../design/objects/joint2.stl) of the ball joint. Insert one red laser into each holder, thread the wires through both the holder and socket, and solder wire extensions so that the lasers can be powered from the Raspberry Pi (~30cm of wire). Use hot glue to secure the lasers in the holder.
   2. Connect the negative wire for the red lasers to the Raspberry Pi ground pin and the positive wires to the GPIO pins as described in the [wiring diagram](../design/wiring.fzz).
   3. Connect the grounds between the Raspberry Pi and Arduino Nano, so they share a common ground.
   4. Connect the Raspberry Pi GPIO pins to the Arduino Nano pins to control the acoustic trap motion, as in the [wiring diagram](../design/wiring.fzz).
   5. Connect the camera ribbon cable to the camera and Raspberry Pi.

4. **Set up the software**
   1. Flash the SD card with [Raspberry Pi OS](https://www.raspberrypi.com/software/) and insert it into the Raspberry Pi.
   2. Connect the touchscreen to the Raspberry Pi.
   3. Boot up the Raspberry Pi, and clone the repository to the device.

        ```bash
        git clone https://github.com/OpenQuantumDesign/outreach.git
        ```

   4. Install a code editor, such as Visual Studio Code (e.g., `sudo apt install code`).
   5. Create a virtual environment, e.g., with `pip` or `venv`, and install all dependencies.
   6. Ensure the device configuration matches the GPIO pins used for the trap and laser.
   7. Test that images are correctly captured by the camera, and that the laser intensities and trap positions are controllable via the software modules.

        ```bash
        # activate the virtual environment
        source .venv/bin/activate

        # start the camera stream and detach
        python src/gui/camera_stream.py &

        # start the main interface server
        python src/gui/main.py &
        ```

   8. Launch a browser in kiosk mode

        ```bash
        chromium --kiosk http://127.0.0.1:8080
        ```

5. **Put it all together:**
   1. Once everything is tested and working, package it into the 3D printed enclosure, using the electronics plate to screw down, e.g., the Raspberry Pi, Arduino Nano, and driver.
   2. Have fun teaching about trapped ion quantum computers!
