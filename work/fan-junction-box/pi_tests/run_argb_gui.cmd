@echo off
rem Copy argb_gui.py to the Pi and start it (open http://pihole:8750; Ctrl-C here stops it).
type "%~dp0argb_gui.py" | ssh brian@pihole "cat > ~/argb_gui.py && echo copied"
ssh -t brian@pihole "[ -e /dev/spidev0.0 ] || { echo turning SPI on for this boot; sudo dtparam spi=on; sleep 1; }; python3 ~/argb_gui.py"
