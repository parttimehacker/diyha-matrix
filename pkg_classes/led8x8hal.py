#!/usr/bin/python3

""" Control the display of an Adafruit 8x8 LED backpack """

# MIT License
#
# Copyright (c) 2019 Dave Wilson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import time
from threading import Thread
import logging
import logging.config

import board
import busio

# Import the HT16K33 LED matrix module.

from adafruit_ht16k33 import matrix

# import the display applications

from .led8x8idle import Led8x8Idle
from .led8x8flash import Led8x8Flash
from .led8x8fibonacci import Led8x8Fibonacci
from .led8x8wopr import Led8x8Wopr
from .led8x8life import Led8x8Life

# Color values as convenient globals.

OFF = 0
GREEN = 1
RED = 2
YELLOW = 3

# state machine modes

IDLE_STATE = 0
DEMO_STATE = 1
SECURITY_STATE = 2

# display modes

FIRE_MODE = 0
PANIC_MODE = 1
FIBONACCI_MODE = 2
WOPR_MODE = 3
LIFE_MODE = 4

SLEEP_TIME = [ 0.2, 0.2, 0.2, 0.2, 0.5 ]

class ModeController:
    """ control changing modes. note Fire and Panic are externally controlled. """

    def __init__(self,):
        """ create mode control variables """
        self.machine_state = DEMO_STATE
        self.current_mode = FIBONACCI_MODE
        self.last_mode = LIFE_MODE
        self.start_time = time.time()

    def set_state(self, state):
        """ set the display mode """
        self.machine_state = state

    def get_state(self,):
        """ get the display mode """
        return self.machine_state

    def set_mode(self, mode):
        """ set the display mode """
        self.last_mode = self.current_mode
        self.current_mode = mode
        self.start_time = time.time()

    def restore_mode(self,):
        """ set or override the display mode """
        self.current_mode = self.last_mode
        self.start_time = time.time()

    def get_mode(self,):
        """ get current the display mode """
        return self.current_mode

    def evaluate(self,):
        """ initialize and start the fibinnocci display """
        now_time = time.time()
        elapsed = now_time - self.start_time
        if elapsed > 60:
            self.last_mode = self.current_mode
            self.current_mode = self.current_mode + 1
            self.start_time = now_time
            if self.current_mode > LIFE_MODE:
                self.current_mode = FIBONACCI_MODE
#pylint: disable=too-many-instance-attributes

class Led8x8HAL:
    """ Idle or sleep pattern """

    def __init__(self, logging_file):
        """ create initial conditions and saving display and I2C lock """
        logging.config.fileConfig(fname=logging_file, disable_existing_loggers=False)
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        # Create the I2C interface.
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the matrix class.
        self.matrix8x8 = matrix.Matrix8x8x2(i2c,auto_write=True)
        self.matrix8x8.fill(0)
        self.mode_controller = ModeController()
        self.idle = Led8x8Idle(self.matrix8x8)
        self.fire = Led8x8Flash(self.matrix8x8, RED)
        self.panic = Led8x8Flash(self.matrix8x8, YELLOW)
        self.fib = Led8x8Fibonacci(self.matrix8x8)
        self.wopr = Led8x8Wopr(self.matrix8x8)
        self.life = Led8x8Life(self.matrix8x8)
        self.error_count = 0

    def reset(self,):
        """ initialize to starting state and set brightness """
        self.mode_controller.set_state(DEMO_STATE)
        self.mode_controller.set_mode(FIBONACCI_MODE)

    def display_thread(self,):
        """ display the series as a 64 bit image with alternating colored pixels """
        while True:
            try:
                mode = self.mode_controller.get_mode()
                time.sleep(SLEEP_TIME[mode])
                if mode == FIRE_MODE:
                    self.fire.update()
                elif mode == PANIC_MODE:
                    self.panic.update()
                else:
                    state = self.mode_controller.get_state()
                    if state == SECURITY_STATE:
                        self.matrix8x8.fill(0)
                    elif state == IDLE_STATE:
                        time.sleep(0.5)
                        self.idle.update()
                    else: #demo
                        if mode == FIBONACCI_MODE:
                            self.fib.update()
                        elif mode == WOPR_MODE:
                            self.wopr.update()
                        elif mode == LIFE_MODE:
                            self.life.update()
                        self.mode_controller.evaluate()
            #pylint: disable=broad-except
            except Exception as ex:
                self.logger.debug('Led8x8Controller: thread exception: %s %s', str(ex),
                            str(self.error_count))
                print("led8x8 exception")
                self.error_count += 1
                if self.error_count < 10:
                    time.sleep(1.0)
                    self.matrix8x8.begin()
                else:
                    break

    def set_mode(self, mode, override=False):
        """ set display mode """
        if override:
            self.mode_controller.set_mode(mode)
        current_mode = self.mode_controller.get_mode()
        if current_mode in (FIRE_MODE, PANIC_MODE):
            return
        self.mode_controller.set_mode(mode)

    def restore_mode(self,):
        """ return to last mode; usually after idle, fire or panic """
        self.mode_controller.restore_mode()

    def set_state(self, state):
        """ set the machine state """
        self.mode_controller.set_state(state)
        if state == IDLE_STATE:
            self.matrix8x8.brightness = 0.1
        else:
            self.matrix8x8.brightness = 1.0

    def get_state(self,):
        """ get the current machine state """
        return self.mode_controller.get_state()

    def update_motion(self, topic):
        """ update the countdown timer for the topic (room)"""
        self.motion.motion_detected(topic)

    def run(self):
        """ start the display thread and make it a daemon """
        display = Thread(target=self.display_thread)
        display.daemon = True
        display.start()

if __name__ == '__main__':
    sys.exit()

