# some micropython code from ChatGPT to create a bluetooth keyboard
# that sends a single char
# Doesn't work yet.

from machine import Pin, Timer
import ubluetooth
import time
import struct


class BLEPeripheral:
    def __init__(self):
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)

        # Define service and characteristic
        self.service_uuid = ubluetooth.UUID(
            "6AABF645-4E9D-49B4-93A6-063C9FDFA8A8")
        self.char_uuid = ubluetooth.UUID(
            "72F8FFC9-C962-415A-87FD-7A4EEBF74019")

        # Add service and characteristic
        self.service = (self.service_uuid, (self.char_uuid,))
        self.services = (self.service,)
        self.handles = self.ble.gatts_register_services(self.services)

        self._advertise()

        self.button = Pin(0, Pin.IN, Pin.PULL_UP)  # Assuming a button on GPIO0
        self.debounce_timer = Timer(-1)  # Timer for debouncing
        self.button_pressed = False
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self._on_button_press)

    def _advertise(self):
        name = bytes("BLE-Peripheral", 'utf-8')
        self.ble.gap_advertise(100_000, adv_data=name)

    def _irq(self, event, data):
        print(event, data)
        if event == 1:
            '''Central disconnected'''
            self.connected()
            self.led(1)

        elif event == 2:
            '''Central disconnected'''
            self.advertiser()
            self.disconnected()

        elif event == 3:
            '''New message received'''
            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode('UTF-8').strip()
            print(message)
            if message == '1':
                self.send('test')

    def _on_button_press(self, pin):
        if not self.button_pressed:
            self.button_pressed = True
            self.debounce_timer.init(
                mode=Timer.ONE_SHOT, period=200, callback=self._debounce_handler)

    def _debounce_handler(self, timer):
        if self.button.value() == 0:  # Button still pressed
            self.send_message(b'\x01')  # Sending a single byte (0x01)
        self.button_pressed = False

    def send_message(self, data):
        # Get the value handle for the characteristic
        value_handle = self.handles[0][1]
        # Notify central of the data
        self.ble.gatts_notify(0, value_handle, data)


# Initialize Peripheral
ble_peripheral = BLEPeripheral()

while True:
    time.sleep_ms(100)
