# Drive a NeoPixel 8x8 matrix (https://www.adafruit.com/product/1487)
# from a Raspberry Pi Pico (https://www.raspberrypi.org/documentation)
# RGB colors cycle up and down in relatively prime steps

import board
import neopixel
import time

num_pixels = 8 * 8 # Adafruit 8x8 NeoPixel matrix: 
loop_delay = 0.02  # color refresh rate. 0.01 = too fast.  0.05 = too slow

pixels = neopixel.NeoPixel(board.GP19, num_pixels)
pixels.brightness = 0.5  # reduce from 1.0 b/c all pixels are on

class ColorComponent:
    ''' A color component (e.g. r, g, b) that cycles up and down
        between 0 and 255 with a particular step size. '''
    def __init__(self, start, step):
        self.value : int  = start
        self.step : int  = step
        self.direction : int = 1  # control the direction of change
                                  # 1 = up, -1 = down
    
    def update(self):
        self.value = self.value + self.direction * self.step
        if not (0 <= self.value <= 255):   # if not in range
             self.value = max(0, min(255, self.value))  # clamp
             self.direction = -self.direction # and reverse direction 
        # print(self.value)

    # TODO:  figure out why __int__ doesn't work.  Micropython maybe?
    # def __int__(self):
    #     return self.value
    
r: ColorComponent = ColorComponent(128, 2)  # use relatively prime steps
g: ColorComponent = ColorComponent(0, 3)    # to avoid color repetition
b: ColorComponent = ColorComponent(128, 5)

while True:
    for cc in [r,g,b]:
        cc.update()

    pixels.fill((r.value, g.value, b.value))  # have to use .value  (__int__ doesn't work)
    time.sleep(loop_delay)
