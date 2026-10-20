"""Disposable synthetic artwork for local image-preview acceptance."""
from pathlib import Path
import struct,zlib
w,h=512,128
pixels=bytearray(bytes((16,29,46,255))*(w*h))
font={'L':['10000']*6+['11111'],'A':['01110','10001','10001','11111','10001','10001','10001'],
      'B':['11110','10001','10001','11110','10001','10001','11110'],
      'R':['11110','10001','10001','11110','10100','10010','10001'],
      'X':['10001','10001','01010','00100','01010','10001','10001']}
for j,ch in enumerate('LAB RAX'):
    for y,row in enumerate(font.get(ch,['00000']*7)):
        for x,bit in enumerate(row):
            if bit=='1':
                for dy in range(9):
                    for dx in range(9):
                        index=((30+y*9+dy)*w+55+j*57+x*9+dx)*4;pixels[index:index+4]=bytes((211,232,255,255))
def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
raw=b''.join(b'\0'+pixels[y*w*4:(y+1)*w*4] for y in range(h))
Path('work/assembly-instances/preview-artwork.png').write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
