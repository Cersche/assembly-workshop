"""Multi-color faceplate export: reduction, clean-up and (when OpenSCAD is present) watertight STLs.

Uses a disposable temp folder and a synthetic image; never touches user data.
"""
import base64
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zipfile
import zlib

import assembly_records
import faceplate_color as fc
import mesh_revision

ROOT = Path(__file__).resolve().parent


def png(width, height, pixel):
    rows = b''.join(b'\x00' + b''.join(bytes(pixel(x, y)) for x in range(width)) for y in range(height))

    def chunk(kind, body):
        return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body) & 0xffffffff)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def logo(x, y):
    if 10 < x < 60 and 10 < y < 40:
        return (220, 30, 30, 255)
    if 80 < x < 150 and 20 < y < 30:
        return (240, 240, 240, 255)
    if x == 170 and y % 2:
        return (0, 0, 200, 255)      # one-pixel dotted line: thinner than 0.8 mm
    return (0, 0, 0, 0)


class FaceplateColorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fc-test-')
        self.dir = Path(self.temp.name)
        data = png(200, 50, logo)
        asset = assembly_records.save_artwork(self.dir, {'data_url': 'data:image/png;base64,' + base64.b64encode(data).decode()})
        self.art = {'sha256': asset['sha256'], 'name': 'logo.png', 'x': .5, 'y': .5, 'scale': .5,   # 68 mm wide: one pixel = 0.34 mm
                    'filament': {'count': 4, 'style': 'inlay', 'colors': []}}

    def tearDown(self):
        self.temp.cleanup()

    def test_png_round_trip_with_filters(self):
        w, h, rgba = fc.decode_png(fc.encode_png(3, 2, bytes(range(18))))
        self.assertEqual((w, h), (3, 2))
        self.assertEqual(bytes(rgba[:8]), bytes([0, 1, 2, 255, 3, 4, 5, 255]))

    def test_settings_validation(self):
        bad = dict(self.art, filament={'count': 9})
        with self.assertRaises(ValueError):
            assembly_records.appearance({'artwork': bad})
        saved = assembly_records.appearance({'artwork': self.art})['artwork']
        self.assertEqual(saved['filament'], {'count': 4, 'style': 'inlay', 'colors': []})
        self.assertEqual(saved['mode'], 'preview-only')

    def test_preview_reduces_and_cleans(self):
        r = fc.preview(self.art, self.dir)
        self.assertIsNone(r['palette'][0])              # transparent area = faceplate color
        self.assertEqual(len(r['bodies']), 2)           # dotted line removed as too thin
        self.assertTrue(any('thinner' in w for w in r['warnings']))
        self.assertTrue(r['exportable'])

    def test_same_filament_merges_bodies(self):
        first = fc.preview(self.art, self.dir)
        same = dict(self.art, filament={'count': 4, 'style': 'inlay', 'colors': ['#4e75a3', '#ff0000', '#ff0000', '#0000ff']})
        r = fc.preview(same, self.dir)
        self.assertEqual(len(r['bodies']), len(first['bodies']) - 1)
        self.assertIn(2, r['merged'])

    def test_export_is_watertight_and_conserves_volume(self):
        try:
            mesh_revision.compiler()
        except ValueError:
            self.skipTest('OpenSCAD not installed')
        source = (ROOT / 'pi4_baseline.scad').read_text(encoding='utf-8')
        volumes = {}
        for style in ('inlay', 'emboss'):
            art = dict(self.art, filament=dict(self.art['filament'], style=style))
            with zipfile.ZipFile(io.BytesIO(fc.export(art, source, {'test': True}, self.dir))) as z:
                report = json.loads(z.read('revision.json'))
                self.assertIn('base.stl', z.namelist())
                for name in report['sha256']:
                    path = self.dir / name
                    path.write_bytes(z.read(name))
                    mesh_revision.read_mesh(path, name)   # closed, consistent, positive volume
                volumes[style] = report['mesh']
        inlay_total = sum(v['signed_volume_mm3'] for v in volumes['inlay'].values())
        self.assertAlmostEqual(inlay_total, volumes['emboss']['base']['signed_volume_mm3'], delta=0.05)


if __name__ == '__main__':
    unittest.main()
