import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

print("Starting")

keyboard = KMKKeyboard()

keyboard.col_pins = (
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15
)
keyboard.row_pins = (
    board.GP20,
    board.GP19,
    board.GP18,
    board.GP17,
    board.GP16
)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [KC.A, KC.B, KC.C, KC.D, KC.BSPACE,
     KC.N7, KC.N8, KC.N9, KC.E, KC.F13,
     KC.N4, KC.N5, KC.N6, KC.F, KC.F14,
     KC.N1, KC.N2, KC.N3, KC.ENTER, KC.F15,
     KC.N0, KC.NO, KC.DOT, KC.NO, KC.F16
     ]
]

if __name__ == '__main__':
    keyboard.go()
