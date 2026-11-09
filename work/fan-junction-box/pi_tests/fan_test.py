#!/usr/bin/env python3
"""CT200 connection test, run on the Pi (2026-11-09).

Checks the 200 mm fan wiring from docs/devices/fan-200mm.md:
  TACH  CT200 pin 3 -> GPIO6  / header pin 31 (Pi's own pull-up)
  PWM   CT200 pin 4 -> GPIO12 / header pin 32
  Ground tie: brick GND joined to Pi GND (pin 39) - required for both.

No config changes or reboot are needed. The script uses plain GPIO
(lgpio, part of Raspberry Pi OS), not the hardware-PWM overlay:
  0 %   = PWM pin driven low
  50 %  = lgpio software PWM at 10 kHz (rough; the fan expects 25 kHz)
  100 % = PWM pin let go (the fan's own pull-up = full speed)
It always ends with the PWM pin let go, so the fan is left at full speed.

Run:  python3 fan_test.py
"""
import sys
import time

try:
    import lgpio
except ImportError:
    sys.exit("lgpio missing: sudo apt install python3-lgpio")

TACH = 6
PWM = 12
PULSES_PER_REV = 2   # standard PC fan tach
SETTLE_S = 8
MEASURE_S = 5


def open_chip():
    seen = []
    for n in range(8):  # Pi 5 on older kernels uses gpiochip4
        try:
            h = lgpio.gpiochip_open(n)
        except Exception:
            continue
        info = lgpio.gpio_get_chip_info(h)  # (status, lines, name, label)
        label = f"{info[2]} {info[3]}"
        seen.append(f"{n}: {label} ({info[1]} lines)")
        if "pinctrl" in label:
            return h, n, label
        lgpio.gpiochip_close(h)
    sys.exit("No Pi GPIO chip found. Chips seen: " + "; ".join(seen))


def rpm(cb):
    cb.reset_tally()
    time.sleep(MEASURE_S)
    return cb.tally() * 60.0 / PULSES_PER_REV / MEASURE_S


def pwm_release(h):
    lgpio.gpio_free(h, PWM)
    lgpio.gpio_claim_input(h, PWM, lgpio.SET_PULL_NONE)


def main():
    h, n, label = open_chip()
    print(f"GPIO chip {n} ({label})")

    # 1. Is the PWM wire there? With a pull-down on our side, the fan's
    #    internal pull-up should still make the line read 1.
    lgpio.gpio_claim_input(h, PWM, lgpio.SET_PULL_DOWN)
    time.sleep(0.05)
    pwm_level = lgpio.gpio_read(h, PWM)
    print(f"1. PWM line (GPIO12, pin 32) with Pi pull-down: {pwm_level}"
          f"  -> {'fan pull-up seen, wire + ground OK' if pwm_level else 'reads 0: wire, ground tie or fan power missing'}")
    pwm_release(h)

    # 2. Tach input with the Pi's pull-up, count falling edges.
    lgpio.gpio_claim_alert(h, TACH, lgpio.FALLING_EDGE, lgpio.SET_PULL_UP)
    lgpio.gpio_set_debounce_micros(h, TACH, 200)
    cb = lgpio.callback(h, TACH, lgpio.FALLING_EDGE)

    results = {}
    try:
        for name in ("100 %", "0 %", "50 %", "100 %"):
            if name == "0 %":
                lgpio.gpio_free(h, PWM)
                lgpio.gpio_claim_output(h, PWM, 0)
            elif name == "50 %":
                lgpio.tx_pwm(h, PWM, 10000, 50)
            else:
                if "50 %" in results:
                    lgpio.tx_pwm(h, PWM, 0, 0)  # stop software PWM
                pwm_release(h)
            print(f"   PWM {name}: settling {SETTLE_S} s ...", flush=True)
            time.sleep(SETTLE_S)
            r = rpm(cb)
            results[name] = r
            print(f"   PWM {name}: {r:.0f} RPM")
    finally:
        try:
            lgpio.tx_pwm(h, PWM, 0, 0)
        except Exception:
            pass
        pwm_release(h)  # leave the fan at full speed
        cb.cancel()

    full, low = results["100 %"], results["0 %"]
    print()
    if max(results.values()) > 3000:  # a 200 mm fan runs well under 1500 RPM
        print("2./3. TACH reads NOISE, not a fan (over 3000 RPM). Usual cause: no ground tie"
              " between brick GND and Pi GND (pin 39), or the tach wire not on pin 31.")
        lgpio.gpiochip_close(h)
        return
    print(f"2. TACH (GPIO6, pin 31): {'OK' if full > 100 else 'NO SIGNAL (check pin 31 wire and the ground tie)'}"
          f"  full speed {full:.0f} RPM")
    if full > 100:
        print(f"3. PWM control: {'OK' if low < 0.7 * full else 'NO EFFECT (check pin 32 wire)'}"
              f"  0 % = {low:.0f} RPM, 50 % = {results['50 %']:.0f} RPM,"
              f" {'fan stops at 0 %' if low < 50 else 'fan does not stop at 0 %'}")
    else:
        print("3. PWM control: can't judge without a tach signal; watch/listen to the fan during the 0 % step")
    lgpio.gpiochip_close(h)


if __name__ == "__main__":
    main()
