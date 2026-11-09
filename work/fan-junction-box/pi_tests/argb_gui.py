#!/usr/bin/env python3
"""CT200 ARGB colour picker, served from the Pi 4 (2026-11-09). Stdlib + spidev.

Open http://pihole:8750 on the LAN. Same SPI drive as argb_test.py
(GPIO10 / pin 19, 6.4 MHz, 8 SPI bits per WS2812 bit). The current frame is
resent every 0.2 s so a missed frame shows up as flicker, not as nothing.
Stop with Ctrl-C (LEDs go off).

Run:  python3 argb_gui.py
"""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

try:
    import spidev
except ImportError:
    sys.exit("spidev missing: sudo apt install python3-spidev")

PORT = 8750
MAX_LEVEL = 128  # brightness cap (Pi 5 V budget)
ONE, ZERO = 0b11111000, 0b11000000
RESET = bytes(64)

state = {"hex": "ff0000", "level": 40, "count": 48, "order": "GRB", "led": 0, "on": True}
lock = threading.Lock()
spi = spidev.SpiDev()


def frame():
    s = state
    r, g, b = (int(s["hex"][i:i + 2], 16) * s["level"] // 255 for i in (0, 2, 4))
    rgb = {"R": r, "G": g, "B": b}
    color = [rgb[c] for c in s["order"]] if s["on"] else [0, 0, 0]
    out = bytearray(RESET)
    for i in range(s["count"]):
        px = color if s["led"] in (0, i + 1) else [0, 0, 0]
        for byte in px:
            for bit in range(7, -1, -1):
                out.append(ONE if byte >> bit & 1 else ZERO)
    out += RESET
    return bytes(out)


def refresher():
    while True:
        with lock:
            spi.writebytes2(frame())
        time.sleep(0.2)


PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>CT200 ARGB</title>
<style>body{font:16px system-ui;background:#111;color:#eee;max-width:420px;margin:16px auto;padding:0 16px}
label{display:block;margin:14px 0 4px}input,select,button{font:inherit}
.p button{width:23%;height:44px;margin:1%;border:0;border-radius:6px;color:#000;font-weight:600}
#c{width:100%;height:60px;border:0}#s{margin-top:16px;color:#9c9}</style>
<h2>CT200 ARGB</h2>
<div class=p>
<button style=background:#f00 onclick="pick('ff0000')">Red</button><button style=background:#0f0 onclick="pick('00ff00')">Green</button><button style=background:#00f;color:#fff onclick="pick('0000ff')">Blue</button><button style=background:#fff onclick="pick('ffffff')">White</button>
<button style=background:#ff0 onclick="pick('ffff00')">Yellow</button><button style=background:#0ff onclick="pick('00ffff')">Cyan</button><button style=background:#f0f onclick="pick('ff00ff')">Magenta</button><button style=background:#555;color:#fff onclick="off()">Off</button></div>
<label>Custom colour</label><input type=color id=c value="#ff0000" oninput="pick(this.value.slice(1))">
<label>Brightness <span id=lv>40</span> / MAXL</label><input type=range id=l min=0 max=MAXL value=40 style=width:100% oninput="lv.textContent=this.value;send({level:this.value})">
<label>Light only LED # (0 = all)</label><input type=number id=n min=0 max=200 value=0 oninput="send({led:this.value})"> <button onclick="n.value=Math.max(0,+n.value-1);send({led:n.value})">-</button> <button onclick="n.value=+n.value+1;send({led:n.value})">+</button>
<label>LEDs to drive</label><input type=number min=1 max=200 value=48 oninput="send({count:this.value})">
<label>Colour order</label><select oninput="send({order:this.value})"><option>GRB<option>RGB<option>BRG<option>RBG<option>GBR<option>BGR</select>
<div id=s></div>
<script>
function send(p){fetch('/set?'+new URLSearchParams(p)).then(r=>r.json()).then(j=>s.textContent='Sent: '+JSON.stringify(j)).catch(e=>s.textContent='Error: '+e)}
function pick(h){c.value='#'+h;send({hex:h,on:1})}
function off(){send({on:0})}
</script>"""


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urlparse(self.path)
        if u.path == "/set":
            q = {k: v[0] for k, v in parse_qs(u.query).items()}
            with lock:
                if "hex" in q and len(q["hex"]) == 6:
                    state["hex"] = q["hex"].lower()
                if "level" in q:
                    state["level"] = max(0, min(MAX_LEVEL, int(q["level"])))
                if "count" in q:
                    state["count"] = max(1, min(200, int(q["count"])))
                if "led" in q:
                    state["led"] = max(0, int(q["led"]))
                if q.get("order") in ("GRB", "RGB", "BRG", "RBG", "GBR", "BGR"):
                    state["order"] = q["order"]
                if "on" in q:
                    state["on"] = q["on"] == "1"
                body = json.dumps(state).encode()
            ctype = "application/json"
        else:
            body = PAGE.replace("MAXL", str(MAX_LEVEL)).encode()
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def main():
    try:
        spi.open(0, 0)
    except FileNotFoundError:
        sys.exit("No /dev/spidev0.0: SPI is off (sudo dtparam spi=on)")
    spi.max_speed_hz = 6400000
    spi.mode = 0
    threading.Thread(target=refresher, daemon=True).start()
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), H)
    print(f"ARGB picker on http://pihole:{PORT}  (Ctrl-C to stop)", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        with lock:
            state["on"] = False
            spi.writebytes2(frame())
        print("Stopped, LEDs off.")


if __name__ == "__main__":
    main()
