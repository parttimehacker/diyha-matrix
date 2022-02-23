#!/usr/bin/python3

""" Display full screen flash color pattern on an Adafruit 8x8 LED backpack """

PING = 0
PONG = 1

class Led8x8Flash:
    """ flash pattern based on color and time interval  """

    def __init__(self, matrix8x8x2, color):
        """ create initial conditions and saving display and I2C lock """
        self.matrix = matrix8x8x2
        self.alternate = PING
        if color < 0:
            self.color = 0
            raise Exception('color must be greater than 0 color was: {}'.format(color))
        elif color > 3:
            self.color = 3
            raise Exception('color must be less than 3 color was: {}'.format(color))
        else:
            self.color = color

    def reset(self,):
        """ initialize to starting state and set brightness """
        self.alternate = PING

    def set_color(self, color):
        """ initialize to starting state and set brightness """
        if color < 0:
            self.color = 0
            raise Exception('color must be greater than 0 color was: {}'.format(color))
        elif color > 3:
            self.color = 3
            raise Exception('color must be less than 3 color was: {}'.format(color))
        else:
            self.color = color

    def update(self,):
        """ display the series as a 64 bit image with alternating colored pixels """
        if self.alternate == PING:
            self.matrix.fill(self.color)
            self.alternate = PONG
        else:
            self.matrix.fill(0)
            self.alternate = PING
        #self.matrix.show()

if __name__ == '__main__':
    exit()

