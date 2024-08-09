import time
import digitalio
import board
import rotaryio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Rotary encoder
enc = rotaryio.IncrementalEncoder(board.GP14, board.GP15)
lastPosition = 0

# Mute button
btnMute = digitalio.DigitalInOut(board.GP13)
btnMute.direction = digitalio.Direction.INPUT
btnMute.pull = digitalio.Pull.UP
muted = False

# builtin LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# USB device
consumer = ConsumerControl(usb_hid.devices)

# loop
while True:
    # poll encoder position
    position = enc.position
    if position != lastPosition:
        led.value = True
        if lastPosition < position:
            consumer.send(ConsumerControlCode.VOLUME_INCREMENT)
        else:
            consumer.send(ConsumerControlCode.VOLUME_DECREMENT)
        lastPosition = position
        led.value = False
    
    # poll mute button - if current value has changed, send MUTE key
    if btnMute.value != muted:
        muted = btnMute.value
        consumer.send(ConsumerControlCode.MUTE)
        led.value = True
        time.sleep(0.2)
        led.value = False

    time.sleep(0.06)
