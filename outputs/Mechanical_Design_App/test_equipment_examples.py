"""Explicit render acceptance only: fresh temporary data, no bundles/exports/user data."""
import json
from pathlib import Path
import tempfile
import unittest
import equipment
import mesh_revision
from equipment_examples import example_item


class ExampleRenderTests(unittest.TestCase):
    def test_generic_example_renders_closed_meshes(self):
        item = example_item()
        spec = equipment.clean(item['spec'])
        with tempfile.TemporaryDirectory(prefix='equipment-example-acceptance-') as folder:
            rendered = equipment.render(spec, folder)
            self.assertTrue(rendered.is_relative_to(Path(folder)))
            self.assertEqual((rendered / 'equipment.scad').read_text(encoding='utf-8'), equipment.source(spec))
            report = json.loads((rendered / 'revision.json').read_text(encoding='utf-8'))
            self.assertEqual(set(report['parts']), {'tray', 'faceplate'})
            for name in report['parts']:
                mesh = mesh_revision.read_mesh(rendered / (name + '.stl'), name)
                self.assertGreater(mesh['signed_volume_mm3'], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
