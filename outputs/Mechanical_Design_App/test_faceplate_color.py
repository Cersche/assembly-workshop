"""Multi-color faceplate export on wizard-made faceplates (equipment_tray.scad): placement, reduction,
clean-up, keep-clear areas and (when OpenSCAD is present) closed STLs whose volumes add up to the plain plate.

Uses a disposable temp folder, a synthetic image and a synthetic library item; never touches user data.
"""
import base64
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
import zipfile
import zlib

import assembly_records
import equipment
import faceplate_color as fc
import mesh_revision

ROOT = Path(__file__).resolve().parent
SPEC = {'name': 'Color test', 'dev_w': 85, 'dev_d': 56, 'dev_h': 20, 'device_mount': 'inserts', 'joint': 'screw',
        'holes': [[3.5, 3.5], [61.5, 49.5]], 'keystones': [70],
        'ports': [{'label': 'LAN', 'type': 'rj45', 'x': -70, 'z': 20, 'w': 17, 'h': 14, 'r': 1}]}


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
    if x in (170, 171):
        return (0, 0, 200, 255)      # two-pixel line, about 0.6 mm at this size: thinner than 0.8 mm
    return (0, 0, 0, 0)


def colored_boxes(r):
    """Every printed color rectangle in faceplate mm: (x0, x1, z0, z1)."""
    left, top = r['origin']
    cw, ch = r['cell_mm']
    return [(left + x0 * cw, left + x1 * cw, top - y1 * ch, top - y0 * ch) for b in r['bodies'] for x0, y0, x1, y1 in b['rects']]


class FaceplateColorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fc-test-')
        self.dir = Path(self.temp.name)
        self.spec = equipment.clean(SPEC)
        data = png(200, 50, logo)
        asset = assembly_records.save_artwork(self.dir, {'data_url': 'data:image/png;base64,' + base64.b64encode(data).decode()})
        self.art = {'sha256': asset['sha256'], 'name': 'logo.png', 'x': .5, 'y': .5, 'scale': .5,
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

    def test_window_follows_the_44_4_mm_plate(self):
        # Same numbers as rack-studio.js artworkWindow(252, plate_h, 0.025): 18 mm sides, 4 mm top/bottom.
        for u in (1, 2, 3, 5):
            front = fc.plate(dict(self.spec, u=u, keystones=[], ports=[]))
            plate_h = u * 44.45 - 0.05
            self.assertAlmostEqual(front['height_mm'], plate_h)
            self.assertEqual(front['window']['w'], 216)
            self.assertAlmostEqual(front['window']['h'], plate_h - 8)
            self.assertAlmostEqual(front['window']['z'], u * 44.45 / 2)
            self.assertEqual(len([o for o in front['keep_out'] if abs(o['x']) == fc.HOLE_X]), 4 * u)   # four slots per U

    def test_placement_matches_the_rack_view(self):
        # Expected values printed by rack-studio.js artworkRect() for the same window and openings
        # (js-tests/run.js asserts the same numbers), as [centre x, centre z, width, height].
        cases = [(1, [{'x': 60, 'z': 22.225 + 1.75, 'w': 21, 'h': 33.5}, {'x': -70, 'z': 20, 'w': 17, 'h': 14}],
                  {'x': .3, 'y': .6, 'scale': .8}, 2.5, [-12.84, 21.497, 72.8, 29.12]),
                 (2, [{'x': 0, 'z': 44.45 + 1.75, 'w': 21, 'h': 33.5}, {'x': -60, 'z': 70, 'w': 30, 'h': 10}],
                  {'x': .5, 'y': .5, 'scale': 1}, 1, [60.25, 44.45, 80.85, 80.85]),
                 (1, [], {'x': .5, 'y': .5, 'scale': .65}, 4, [0, 22.225, 94.64, 23.66])]
        for u, holes, art, aspect, expected in cases:
            front = {'window': fc.plate(dict(self.spec, u=u, keystones=[], ports=[]))['window'], 'openings': holes}
            left, top, w, h = fc.layout(art, aspect * 100, 100, front)
            for got, want in zip([left + w / 2, top - h / 2, w, h], expected):
                self.assertAlmostEqual(got, want, places=9)

    def test_openings_match_the_template(self):
        found = fc.openings(self.spec)
        self.assertIn({'x': 70.0, 'z': 44.45 / 2 + 1.75, 'w': 21.0, 'h': 33.5}, found)   # golden keystone block
        self.assertIn({'x': -70.0, 'z': 20.0, 'w': 17.0, 'h': 14.0}, found)
        bezel = fc.openings(dict(self.spec, bezel='chamfer', bezel_size=1.5))
        self.assertIn({'x': -70.0, 'z': 20.0, 'w': 20.0, 'h': 17.0}, bezel)

    def test_color_stays_clear_of_openings_and_rack_holes(self):
        # A full-plate opaque image at full size would cover everything without the keep-clear rules.
        data = png(60, 12, lambda x, y: (200, 0, 0, 255) if (x // 6 + y // 6) % 2 else (255, 255, 255, 255))
        asset = assembly_records.save_artwork(self.dir, {'data_url': 'data:image/png;base64,' + base64.b64encode(data).decode()})
        for u in (1, 2):
            s = equipment.clean(dict(SPEC, u=u))
            art = {'sha256': asset['sha256'], 'name': 'checker.png', 'x': .5, 'y': .5, 'scale': 1,
                   'filament': {'count': 3, 'style': 'inlay', 'colors': []}}
            r = fc.reduce(art, self.dir, s)
            self.assertTrue(r['bodies'])
            front = r['plate']
            for x0, x1, z0, z1 in colored_boxes(r):
                self.assertTrue(-126 + fc.EDGE_KEEP <= x0 and x1 <= 126 - fc.EDGE_KEEP)
                self.assertTrue(front['bottom'] + fc.EDGE_KEEP <= z0 and z1 <= front['bottom'] + front['height_mm'] - fc.EDGE_KEEP)
                for o in front['keep_out']:
                    g = fc.OPENING_GAP - 1e-9
                    self.assertFalse(x1 > o['x'] - o['w'] / 2 - g and x0 < o['x'] + o['w'] / 2 + g
                                     and z1 > o['z'] - o['h'] / 2 - g and z0 < o['z'] + o['h'] / 2 + g, (x0, x1, z0, z1, o))

    def test_slot_spec_uses_library_item_and_slot_tray_settings(self):
        (self.dir / 'equipment-library.json').write_text(json.dumps([{'id': 'eq-0123456789ab', 'name': 'Color test', 'span': 1, 'spec': self.spec}]), encoding='utf-8')
        s = fc.slot_spec(self.dir, {'equipment': 'eq-0123456789ab', 'tray': {'u': 2, 'keystones': [-80]}})
        self.assertEqual((s['u'], s['keystones']), (2, [-80.0]))
        self.assertEqual(fc.plate(s)['window']['z'], 44.45)
        with self.assertRaises(ValueError):
            fc.slot_spec(self.dir, {'equipment': 'eq-ffffffffffff'})
        with self.assertRaises(ValueError):
            fc.slot_spec(self.dir, None)

    def test_preview_reduces_and_cleans(self):
        r = fc.preview(self.art, self.dir, self.spec)
        self.assertIsNone(r['palette'][0])              # transparent area = faceplate color
        self.assertEqual(len(r['bodies']), 2)           # dotted line removed as too thin
        self.assertTrue(any('thinner' in w for w in r['warnings']))
        self.assertTrue(r['exportable'])
        self.assertEqual(r['u'], 1)

    def test_same_filament_merges_bodies(self):
        first = fc.preview(self.art, self.dir, self.spec)
        same = dict(self.art, filament={'count': 4, 'style': 'inlay', 'colors': ['#4e75a3', '#ff0000', '#ff0000', '#0000ff']})
        r = fc.preview(same, self.dir, self.spec)
        self.assertEqual(len(r['bodies']), len(first['bodies']) - 1)
        self.assertIn(2, r['merged'])

    def test_color_only_change_changes_export_identity(self):
        source = fc.faceplate_source(self.spec)
        first = fc.reduce(self.art, self.dir, self.spec)
        recolored = fc.reduce(dict(self.art, filament={'count': 4, 'style': 'inlay', 'colors': [None, '#00ff00']}), self.dir, self.spec)
        self.assertEqual(fc.scad(first)[0], fc.scad(recolored)[0])          # same geometry...
        self.assertNotEqual(fc.export_identity(first, source, fc.scad(first)[0]),
                            fc.export_identity(recolored, source, fc.scad(recolored)[0]))   # ...new cache entry
        new_base = fc.reduce(self.art, self.dir, self.spec, '#000000')
        self.assertNotEqual(fc.export_identity(first, source, fc.scad(first)[0]),
                            fc.export_identity(new_base, source, fc.scad(new_base)[0]))

    def test_opaque_image_keeps_faceplate_as_base(self):
        data = png(40, 20, lambda x, y: (255, 255, 255, 255) if x < 30 else (200, 0, 0, 255))
        asset = assembly_records.save_artwork(self.dir, {'data_url': 'data:image/png;base64,' + base64.b64encode(data).decode()})
        art = {'sha256': asset['sha256'], 'name': 'opaque.png', 'x': .5, 'y': .5, 'scale': .5,
               'filament': {'count': 3, 'style': 'inlay', 'colors': []}}
        r = fc.preview(art, self.dir, self.spec, '#123456')
        self.assertIsNone(r['palette'][0])
        self.assertEqual(r['base_hex'], '#123456')
        self.assertEqual(len(r['bodies']), 2)            # white and red are both printed colors
        # Giving white the faceplate filament leaves that area as plain faceplate.
        art['filament']['colors'] = [None, '#123456']
        self.assertEqual(len(fc.preview(art, self.dir, self.spec, '#123456')['bodies']), 1)

    def test_auto_colors_stay_automatic(self):
        auto = fc.preview(self.art, self.dir, self.spec)
        partial = fc.preview(dict(self.art, filament={'count': 4, 'style': 'inlay', 'colors': [None, None, '#00ff00']}), self.dir, self.spec)
        self.assertEqual(partial['palette'][1], auto['palette'][1])
        self.assertEqual(partial['palette'][2], '#00ff00')

    def test_scad_uses_the_generic_plate(self):
        text, names = fc.scad(fc.reduce(self.art, self.dir, self.spec))
        self.assertIn('front_y=-4.0;', text)
        self.assertIn('difference(){color_base();', text)
        self.assertTrue(all(f'module {n}(){{color_clip()union(){{' in text for n in names))
        source = fc.faceplate_source(self.spec)
        self.assertTrue(source.startswith(equipment.source(self.spec)))
        self.assertIn('module color_base()', source)


def openscad():
    try:
        return mesh_revision.compiler()
    except ValueError:
        return None


@unittest.skipUnless(openscad(), 'OpenSCAD is not installed')
class FaceplateColorRenderTests(unittest.TestCase):
    """Real OpenSCAD renders (slow): closed meshes, and inlay base + color bodies = the plain plate."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fc-render-')
        self.dir = Path(self.temp.name)
        asset = assembly_records.save_artwork(self.dir, {'data_url': 'data:image/png;base64,' + base64.b64encode(png(200, 50, logo)).decode()})
        self.art = {'sha256': asset['sha256'], 'name': 'logo.png', 'x': .5, 'y': .5, 'scale': .5,
                    'filament': {'count': 4, 'style': 'inlay', 'colors': []}}

    def tearDown(self):
        self.temp.cleanup()

    def plain_volume(self, files, folder):
        (folder / 'faceplate_source.scad').write_bytes(files['faceplate_source.scad'])
        (folder / 'plain.scad').write_text('use <faceplate_source.scad>\ncolor_base();\n', encoding='utf-8')
        subprocess.run([openscad(), '-o', str(folder / 'plain.stl'), str(folder / 'plain.scad')], capture_output=True, check=True, timeout=600)
        return mesh_revision.read_mesh(folder / 'plain.stl', 'plain')['signed_volume_mm3']

    def check(self, s, style):
        art = dict(self.art, filament=dict(self.art['filament'], style=style))
        data = fc.export(art, s, {'equipment': 'test'}, self.dir)
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            files = {n: z.read(n) for n in z.namelist()}
        report = json.loads(files['revision.json'])
        self.assertEqual(report['status'], 'PROPOSED — UNVALIDATED')
        self.assertEqual(report['faceplate']['u'], s['u'])
        out = self.dir / ('meshes-' + style + str(s['u']))
        out.mkdir()
        volumes = {}
        for name in report['sha256']:
            (out / name).write_bytes(files[name])
            mesh = mesh_revision.read_mesh(out / name, name)    # raises unless closed and valid
            volumes[name] = mesh['signed_volume_mm3']
            if name != 'base.stl':
                lo, hi = mesh['bounds']
                if style == 'inlay':
                    self.assertAlmostEqual(lo[1], -4.0, places=3)
                    self.assertAlmostEqual(hi[1], -4.0 + fc.DEPTH, places=3)
                else:
                    self.assertAlmostEqual(lo[1], -4.0 - fc.DEPTH, places=3)
                    self.assertAlmostEqual(hi[1], -4.0, places=3)
        plain = self.plain_volume(files, out)
        colors = sum(v for n, v in volumes.items() if n != 'base.stl')
        if style == 'inlay':
            self.assertAlmostEqual(volumes['base.stl'] + colors, plain, delta=0.01 * plain / 100)   # 0.01 %
        else:
            self.assertAlmostEqual(volumes['base.stl'], plain, delta=0.01 * plain / 100)
        return report, volumes, plain

    def test_inlay_1u_with_keystone_and_port(self):
        report, volumes, plain = self.check(equipment.clean(SPEC), 'inlay')
        self.assertEqual(len(report['bodies']), 2)
        print('\n1U inlay volumes (mm3):', {k: round(v, 3) for k, v in volumes.items()}, 'plain', round(plain, 3))

    def test_emboss_2u(self):
        report, volumes, plain = self.check(equipment.clean(dict(SPEC, u=2)), 'emboss')
        print('\n2U emboss volumes (mm3):', {k: round(v, 3) for k, v in volumes.items()}, 'plain', round(plain, 3))


if __name__ == '__main__':
    unittest.main()
