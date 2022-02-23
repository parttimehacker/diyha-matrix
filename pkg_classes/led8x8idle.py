#!/usr/bin/python3
""" Display full screen flash color pattern on an Adafruit 8x8 LED backpack """

GREEN = 2

class Led8x8Idle:
    """ Idle or sleep pattern """

    def __init__(self, matrix8x8x2):
        """ create initial conditions and saving display and I2C lock """
        self.matrix = matrix8x8x2
        self.lastx = 0
        self.lasty = 0

    def reset(self,):
        """ initialize to starting state and set brightness """
        self.lastx = 0
        self.lasty = 0
        self.matrix.fill(0)

    def update(self,):
        """ display the series as a 64 bit image with alternating colored pixels """
        self.matrix.fill(0)
        self.matrix[self.lastx, self.lasty] = GREEN
        self.lasty += 1
        if self.lasty > 7:
            self.lasty = 0
            self.lastx += 1
            if self.lastx > 7:
                self.lastx = 0

if __name__ == '__main__':
    exit()

