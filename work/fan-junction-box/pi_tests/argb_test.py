#!/usr/bin/env python3
"""CT200 ARGB test from the Pi 4 over SPI (2026-11-09). No extra libraries.

Wiring (docs/devices/fan-200mm.md): ARGB +5 V -> pin 2, DATA -> GPIO10 / pin 19
(SPI0 MOSI), GND -> pin 34. Data is 3.3 V, direct (no level shifter).

WS2812 bits are sent as SPI bytes at 6.4 MHz: 1 = 0b11111000 (~780 ns high),
0 = 0b11000000 (~310 ns high). Brightness kept low (Pi 5 V budget).
Steps: all red, green, blue, white; then a one-LED chase with numbers so the
LED count can be read off; then off.

Run:  python3 argb_test.py
"""
import sys
import time

try:
    import spidev
except ImportError:
    sys.exit("spidev missing: sudo apt install python3-spidev")

MAX_LEDS = 48     # more than the CT200 can have; extras are ignored by the strip
LEVEL = 40        # of 255
SPEED_HZ = 6400000
ONE, ZERO = 0b11111000, 0b11000000
RESET = bytes(64)  # ~80 us low


def encode(colors):
    out = bytearray(RESET)
    for r, g, b in colors:
        for byte in (g, r, b):  # WS2812 order is GRB
            for i in range(7, -1, -1):
                out.append(ONE if byte >> i & 1 else ZERO)
    out += RESET
    return bytes(out)


def main():
    spi = spidev.SpiDev()
    try:
        spi.open(0, 0)
    except FileNotFoundError:
        sys.exit("No /dev/spidev0.0: SPI is off (sudo dtparam spi=on)")
    spi.max_speed_hz = SPEED_HZ
    spi.mode = 0

    def show(colors):
        spi.writebytes2(encode(colors))

    off = [(0, 0, 0)] * MAX_LEDS
    try:
        for name, c in (("RED", (LEVEL, 0, 0)), ("GREEN", (0, LEVEL, 0)),
                        ("BLUE", (0, 0, LEVEL)), ("WHITE", (LEVEL, LEVEL, LEVEL))):
            print(f"All {name} (4 s) - what colour do you see?", flush=True)
            show([c] * MAX_LEDS)
            time.sleep(4)
        show(off)
        print("Chase: one LED at a time; note the last number that lights a new LED.", flush=True)
        for i in range(MAX_LEDS):
            frame = list(off)
            frame[i] = (LEVEL, LEVEL, LEVEL)
            show(frame)
            print(f"  LED {i + 1}", flush=True)
            time.sleep(0.6)
    finally:
        show(off)
        spi.close()
    print("Done, LEDs off.")


if __name__ == "__main__":
    main()
