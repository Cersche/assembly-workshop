#!/usr/bin/env python3
"""CT200 speed curve with hardware PWM, run on the Pi 4 (2026-11-09).

Needs `dtoverlay=pwm,pin=12,func=4` in /boot/firmware/config.txt (GPIO12 =
PWM0 = /sys/class/pwm/pwmchip0/pwm0) and a reboot. 25 kHz, duty steps
100 -> 0 %, tach on GPIO6 (pin 31) with the Pi pull-up. Ends at 100 %.

Run:  sudo python3 fan_curve.py
"""
import os
import sys
import time

try:
    import lgpio
except ImportError:
    sys.exit("lgpio missing: sudo apt install python3-lgpio")

TACH = 6
PULSES_PER_REV = 2
PERIOD_NS = 40000          # 25 kHz
STEPS = (100, 80, 60, 40, 20, 0, 100)
SETTLE_S = 8
MEASURE_S = 5


def find_pwm():
    base = "/sys/class/pwm"
    chips = sorted(c for c in os.listdir(base) if c.startswith("pwmchip")) if os.path.isdir(base) else []
    if not chips:
        sys.exit("No /sys/class/pwm/pwmchip*: overlay not loaded (check config.txt, reboot)")
    chip = os.path.join(base, chips[0])
    ch = os.path.join(chip, "pwm0")
    if not os.path.isdir(ch):
        with open(os.path.join(chip, "export"), "w") as f:
            f.write("0")
        time.sleep(0.2)
    return ch


def put(ch, name, value):
    with open(os.path.join(ch, name), "w") as f:
        f.write(str(value))


def set_duty(ch, pct):
    put(ch, "duty_cycle", PERIOD_NS * pct // 100)


def open_chip():
    for n in range(8):
        try:
            h = lgpio.gpiochip_open(n)
        except Exception:
            continue
        info = lgpio.gpio_get_chip_info(h)
        if "pinctrl" in f"{info[2]} {info[3]}":
            return h
        lgpio.gpiochip_close(h)
    sys.exit("No Pi GPIO chip found")


def main():
    ch = find_pwm()
    put(ch, "duty_cycle", 0)
    put(ch, "period", PERIOD_NS)
    set_duty(ch, 100)
    put(ch, "enable", 1)
    print(f"Hardware PWM {ch}, 25 kHz")

    h = open_chip()
    lgpio.gpio_claim_alert(h, TACH, lgpio.FALLING_EDGE, lgpio.SET_PULL_UP)
    lgpio.gpio_set_debounce_micros(h, TACH, 1000)
    cb = lgpio.callback(h, TACH, lgpio.FALLING_EDGE)
    try:
        for pct in STEPS:
            set_duty(ch, pct)
            time.sleep(SETTLE_S)
            cb.reset_tally()
            time.sleep(MEASURE_S)
            r = cb.tally() * 60.0 / PULSES_PER_REV / MEASURE_S
            flag = "  <- NOISE?" if r > 3000 else ""
            print(f"   PWM {pct:3d} %: {r:6.0f} RPM{flag}", flush=True)
    finally:
        set_duty(ch, 100)  # leave the fan at full speed
        cb.cancel()
        lgpio.gpiochip_close(h)
    print("Left at 100 %. RPM assumes 2 pulses/rev (UNKNOWN for the CT200).")


if __name__ == "__main__":
    main()
