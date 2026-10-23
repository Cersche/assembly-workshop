"""Wall-mount box spec checks (task 38). The OpenSCAD renders run only when AW_RENDER_TESTS=1 is set."""
import os
import tempfile
import subprocess
import unittest
from pathlib import Path

import mesh_revision
import wall_box as wb

BASE = {'inner': {'w': 120, 'd': 60, 'h': 90}, 'lid_style': 'screw', 'mount_style': 'keyhole'}


def spec(**extra):
    return dict(BASE, **extra)


class WallBoxSpecTests(unittest.TestCase):
    def problems(self, raw):
        with self.assertRaises(wb.WallBoxError) as ctx:
            wb.validate(raw)
        return ' '.join(ctx.exception.problems)

    def test_constants_match_the_template(self):
        self.assertEqual(wb.template_constants(), wb.CONST)

    def test_250_mm_limit_counts_mounts(self):
        self.assertEqual(wb.outer_size(wb.validate(spec(inner={'w': 245, 'd': 60, 'h': 200}))), (250, 65, 205))
        self.assertIn('Outer size X', self.problems(spec(inner={'w': 246, 'd': 60, 'h': 90})))
        self.assertIn('Outer size Z', self.problems(spec(inner={'w': 120, 'd': 60, 'h': 215}, mount_style='tabs')))
        self.assertIn('Outer size Y', self.problems(spec(inner={'w': 120, 'd': 238, 'h': 90}, mount_style='cleat')))

    def test_unknown_keys_and_options_are_refused(self):
        self.assertIn('unknown settings: colour', self.problems(spec(colour='red')))
        self.assertIn('Lid style must be', self.problems(spec(lid_style='magnet')))
        self.assertIn('unknown settings: x', self.problems(spec(cutouts=[{'wall': 'lid', 'type': 'round', 'd': 8, 'u': 0, 'v': 0, 'x': 1}])))

    def test_cutouts_stay_inside_and_apart(self):
        self.assertIn('inside the wall', self.problems(spec(cutouts=[{'wall': 'lid', 'type': 'round', 'd': 10, 'u': 55, 'v': 0}])))
        self.assertIn('overlap', self.problems(spec(cutouts=[{'wall': 'lid', 'type': 'round', 'd': 10, 'u': 0, 'v': 0},
                                                             {'wall': 'lid', 'type': 'rect', 'w': 10, 'h': 10, 'u': 11, 'v': 0}])))
        ok = wb.validate(spec(cutouts=[{'wall': 'lid', 'type': 'round', 'd': 10, 'u': 0, 'v': 0},
                                       {'wall': 'lid', 'type': 'rect', 'w': 10, 'h': 10, 'u': 13, 'v': 0}]))
        self.assertEqual(len(ok['cutouts']), 2)

    def test_cutouts_avoid_box_features(self):
        corner = {'wall': 'lid', 'type': 'round', 'd': 6, 'u': 54, 'v': 39}
        self.assertIn('hits a box feature', self.problems(spec(cutouts=[corner])))
        self.assertIn('hits a box feature', self.problems(spec(mount_style='keyhole', cutouts=[{'wall': 'back', 'type': 'round', 'd': 6, 'u': 40, 'v': 25}])))
        self.assertIn('hits a box feature', self.problems(spec(lid_style='hinge', cutouts=[{'wall': 'left', 'type': 'round', 'd': 6, 'u': 24, 'v': 0}])))

    def test_presets_and_unmeasured_parts(self):
        ok = wb.validate(spec(cutouts=[{'wall': 'bottom', 'type': 'preset', 'preset': 'pg9', 'u': 0, 'v': 0}]))
        self.assertEqual(ok['cutouts'][0], {'wall': 'bottom', 'type': 'gland', 'u': 0, 'v': 0, 'size': 'PG9'})
        self.assertIn('UNKNOWN', self.problems(spec(cutouts=[{'wall': 'lid', 'type': 'preset', 'preset': 'screenbeam_ecb7250', 'u': 0, 'v': 0}])))
        self.assertIn('no known size', self.problems(spec(cutouts=[{'wall': 'lid', 'type': 'preset', 'preset': 'barrel_jack', 'u': 0, 'v': 0}])))
        parts = wb.load_parts()
        self.assertEqual(parts['screenbeam_ecb7250']['size'], [120, 65, 30])

    def test_standoffs(self):
        ok = wb.validate(spec(standoffs=[{'x': -20, 'z': 0, 'height': 6, 'hole': 2.5}]))
        self.assertEqual(ok['standoffs'][0]['outer'], 6.5)
        self.assertIn('taller', self.problems(spec(standoffs=[{'x': 0, 'z': 0, 'height': 59, 'hole': 2.5}])))
        self.assertIn('overlap', self.problems(spec(standoffs=[{'x': 0, 'z': 0, 'height': 5, 'hole': 2.5}, {'x': 3, 'z': 0, 'height': 5, 'hole': 2.5}])))

    def test_source_is_deterministic_and_carries_the_golden_keystone(self):
        s = wb.validate(spec(vents=['top', 'lid'], cutouts=[{'wall': 'bottom', 'type': 'keystone', 'u': 0, 'v': 0}]))
        a, b = wb.scad_source(s, 'body'), wb.scad_source(wb.validate(spec(vents=['lid', 'top'], cutouts=[{'wall': 'bottom', 'type': 'keystone', 'u': 0, 'v': 0}])), 'body')
        self.assertEqual(a, b)
        self.assertIn('ks_tight=0.2;', a)
        self.assertIn('[-10.50,0.60,', a)
        self.assertIn('vents=["lid","top"];', a)
        self.assertIn('cutouts=[["bottom","keystone",0,0,0,0]];', a)
        self.assertNotIn('KS_GOLD=[];', a)

    def test_vents_step_around_cutouts(self):
        s = wb.validate(spec(vents=['left'], cutouts=[{'wall': 'left', 'type': 'gland', 'size': 'PG7', 'u': 0, 'v': 0}]))
        rows = [r for r in wb.vent_avoid(s) if r[0] == 'left']
        r = (12.5 + 8) / 2 + 3
        self.assertIn(('left', -r, -r, r, r), rows)


@unittest.skipUnless(os.environ.get('AW_RENDER_TESTS') == '1', 'set AW_RENDER_TESTS=1 to render with OpenSCAD')
class WallBoxRenderTests(unittest.TestCase):
    def test_every_lid_and_mount_renders_closed(self):
        exe = mesh_revision.compiler()
        with tempfile.TemporaryDirectory() as folder:
            for lid in wb.LIDS:
                for mount in wb.MOUNTS:
                    s = wb.validate(spec(lid_style=lid, mount_style=mount))
                    for part in ['body', 'lid'] + (['cleat'] if mount == 'cleat' else []):
                        with self.subTest(lid=lid, mount=mount, part=part):
                            src, stl = Path(folder, 'box.scad'), Path(folder, f'{lid}-{mount}-{part}.stl')
                            src.write_text(wb.scad_source(s, part), encoding='utf-8', newline='\n')
                            subprocess.run([exe, '-o', str(stl), str(src)], check=True, capture_output=True)
                            mesh_revision.read_mesh(stl, part)  # raises unless closed and consistently wound


if __name__ == '__main__':
    unittest.main()
