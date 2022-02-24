#!/usr/bin/python3

""" Display War Games WOPR pattern on an Adafruit 8x8 LED backpack """

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

import random

BLACK = 0
GREEN = 2
YELLOW = 3
RED = 1

class Led8x8Wopr:
    """ WOPR pattern based on the movie Wargames """

    def __init__(self, matrix8x8x2):
        """ create initial conditions and saving display and I2C lock """
        self.matrix = matrix8x8x2

    def reset(self,):
        """ initialize to starting state and set brightness """
        self.matrix.fill(0)

    def output_row(self, start, finish, color):
        """ display a section of WOPR based on starting and ending rows """
        for xpixel in range(8):
            for ypixel in range(start, finish):
                bit = random.randint(0, 1)
                if bit > 0:
                    self.matrix[xpixel, ypixel] = color
                    
    def update(self,):
        """ display the series as a 64 bit image with alternating colored pixels """
        self.matrix.fill(0)
        for i in range(64):
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            bit = random.randint(0, 3)
            if bit == 2:
                bit = 1
            self.matrix[x,y] = bit
            
    def updateO(self,):
        """ display the series as a 64 bit image with alternating colored pixels """
        self.matrix.fill(0)
        self.output_row(5, 8, RED)
        self.output_row(0, 1, RED)
        self.output_row(2, 4, RED)
        self.output_row(4, 5, YELLOW)
        self.output_row(1, 2, YELLOW)

if __name__ == '__main__':
    exit()

