# Drive a NeoPixel 8x8 matrix
# RGB colors cycle up and down in relatively prime steps

import board
import neopixel
import time

num_pixels = 8 * 8
pixels = neopixel.NeoPixel(board.GP19, num_pixels)
pixels.brightness = 0.5    # all pixels are on in this version, so reduce brightness
loop_delay = 0.02   # time between color changes.  0.01 is too fast.  0.5 is too slow

# starting color 
r = 128
g = 0
b = 128

# control the direction of change
# 1 = up, -1 = down
rdir = 1
gdir = 1
bdir = 1


while True:
    r = r + rdir * 2
    if r < 0:
        r = 0
        rdir = -rdir
    if r > 255:
        r = 255
        rdir = -rdir  

    g = g + gdir * 3
    if g < 0:
        g = 0
        gdir = -gdir
    if g > 255:
        g = 255
        gdir = -gdir 

    b = (b + bdir * 5)
    if b < 0:
        b = 0
        bdir = -bdir
    if b > 255:
        b = 255
        bdir = -bdir 

    # print("(r, g, b): ", (r, g, b))
    pixels.fill((r, g, b))
    time.sleep(loop_delay)
