# Import all board pins.
import time
import board
import busio

GREEN_LED = 1
RED_LED = 2
YELLOW_LED = 3


# Import the HT16K33 LED matrix module.
from adafruit_ht16k33 import matrix

from led8x8flash import Led8x8Flash
from led8x8fibonacci import Led8x8Fibonacci
from led8x8wopr import Led8x8Wopr
from led8x8idle import Led8x8Idle
from led8x8life import Led8x8Life

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the matrix class.

MATRIX = matrix.Matrix8x8x2(i2c)

DISPLAY0 = Led8x8Flash(MATRIX,GREEN_LED)

"""
print("green")
for i in range(3):
    DISPLAY0.update()
    time.sleep(0.5)
    
print("red")
for i in range(3):
    DISPLAY0.set_color(RED_LED)
    DISPLAY0.update()
    time.sleep(0.5)

print("yellow")
for i in range(3):
    DISPLAY0.set_color(YELLOW_LED)
    DISPLAY0.update()
    time.sleep(0.5)

DISPLAY1 = Led8x8Fibonacci(MATRIX)

for i in range(32):
    DISPLAY1.update()
    time.sleep(0.2)

DISPLAY2 = Led8x8Wopr(MATRIX)

for i in range(32):
    DISPLAY2.update()
    time.sleep(0.1)
    
DISPLAY3 = Led8x8Idle(MATRIX)

for i in range(32):
    DISPLAY3.update()
    time.sleep(0.5)
"""    
DISPLAY4 = Led8x8Life(MATRIX)

for i in range(123):
    DISPLAY4.update()
    time.sleep(0.5)