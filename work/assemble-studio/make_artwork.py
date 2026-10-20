"""Generate original synthetic artwork for disposable local preview acceptance."""
from pathlib import Path
import struct
import zlib
letters={'L':['10000','10000','10000','10000','10000','10000','11111'],'A':['01110','10001','10001','11111','10001','10001','10001'],'B':['11110','10001','10001','11110','10001','10001','11110'],'R':['11110','10001','10001','11110','10100','10010','10001'],'X':['10001','10001','01010','00100','01010','10001','10001'],' ':['00000']*7}
text='LAB RAX';scale=6;width=len(text)*6*scale;height=9*scale
raw=bytearray()
for y in range(height):
    raw.append(0)
    for x in range(width):
        letter=x//(6*scale);gx=x//scale%6;gy=y//scale-1
        on=0<=gy<7 and gx<5 and letters[text[letter]][gy][gx]=='1'
        raw.extend((170,240,245,255) if on else (0,0,0,0))
def chunk(kind,data):return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data)&0xffffffff)
data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!2I5B',width,height,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')
Path(__file__).with_name('Local_Test_Artwork.png').write_bytes(data)
