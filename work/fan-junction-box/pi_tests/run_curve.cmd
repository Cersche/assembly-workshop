@echo off
rem Copy fan_curve.py to the Pi over ssh (no scp) and run it; reboot instead if PWM isn't active yet.
type "%~dp0fan_curve.py" | ssh brian@pihole "cat > ~/fan_curve.py && echo copied"
ssh -t brian@pihole "grep -n pwm,pin=12 /boot/firmware/config.txt; if [ -e /sys/class/pwm/pwmchip0 ]; then sudo python3 ~/fan_curve.py; else echo PWM-NOT-ACTIVE-REBOOTING; sudo reboot; fi"
