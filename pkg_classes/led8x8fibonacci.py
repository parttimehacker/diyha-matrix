#!/usr/bin/python3
""" Display the fibonacci series as a 64 bit pattern on an Adafruit 8x8 LED backpack """

import time

UPDATE_RATE_SECONDS = 0.2

LARGEST_64_BIT_FIBONACCI = 7540113804746346429

class Led8x8Fibonacci:
    """ fibinocci pattern from 1 to largest 64 bit representation  """

    def __init__(self, matrix8x8x2):
        """ create initial conditions and saving display and I2C lock """
        self.matrix = matrix8x8x2
        self.iterations = 0
        self.fib1 = 1
        self.fib2 = 1
        self.fib3 = 2

    def reset(self,):
        """ initialize to starting state and set brightness """
        self.iterations = 0
        self.fib1 = 1
        self.fib2 = 1
        self.fib3 = 2

    def update(self,):
        """ display the series as a 64 bit image with alternating colored pixels """
        self.matrix.fill(0)
        for ypixel in range(0, 8):
            for xpixel in range(0, 8):
                self.iterations += 1
                if self.iterations >= 4:
                    self.iterations = 1
                reg = self.fib3 >> (8 * xpixel)
                bit = reg & (1 << ypixel)
                if bit > 0:
                    self.matrix[xpixel, ypixel] = 2 # self.iterations
        self.fib1 = self.fib2
        self.fib2 = self.fib3
        self.fib3 = self.fib1 + self.fib2
        if self.fib3 > LARGEST_64_BIT_FIBONACCI:
            self.fib1 = 1
            self.fib2 = 1
            self.fib3 = 2

if __name__ == '__main__':
    exit()

