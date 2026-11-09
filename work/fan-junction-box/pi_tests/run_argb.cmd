@echo off
rem Copy argb_test.py to the Pi over ssh and run it; turns SPI on for this boot if it's off.
type "%~dp0argb_test.py" | ssh brian@pihole "cat > ~/argb_test.py && echo copied"
ssh -t brian@pihole "[ -e /dev/spidev0.0 ] || { echo turning SPI on for this boot; sudo dtparam spi=on; sleep 1; }; python3 ~/argb_test.py"
