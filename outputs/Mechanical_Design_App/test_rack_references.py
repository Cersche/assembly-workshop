"""Source fidelity, integrity rejection, and HTTP routing without a live socket."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import zipfile

import rack_references
from app import make_handler

CORE = '{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}'
PROJECT = Path(__file__).resolve().parents[2]


class RackReferenceTests(unittest.TestCase):
    def test_every_component_retains_exact_source_coordinates_and_indices(self):
        catalog = json.loads(rack_references.asset('/rack-references/catalog.json')[0])
        count = 0
        self.assertFalse(catalog['manufacturing_geometry_supported'])
        self.assertIn('Brian supplied', catalog['m6_note'])
        for ref in catalog['references']:
            path = PROJECT/'work/rack-geometry-recovery/sources'/ref['source_file']
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),ref['source_sha256'])
            with zipfile.ZipFile(path) as archive:
                for c in ref['components']:
                    model = ET.fromstring(archive.read(c['source_member']))
                    obj = next(o for o in model.findall(CORE+'resources/'+CORE+'object') if o.get('id')==c['id'])
                    vertices = [[float(v.get(k)) for k in ('x','y','z')] for v in obj.findall(CORE+'mesh/'+CORE+'vertices/'+CORE+'vertex')]
                    triangles = [[int(t.get(k)) for k in ('v1','v2','v3')] for t in obj.findall(CORE+'mesh/'+CORE+'triangles/'+CORE+'triangle')]
                    geometry = json.loads(rack_references.asset(c['url'])[0])
                    self.assertEqual(geometry,{'vertices':vertices,'triangles':triangles})
                    self.assertEqual(len(triangles),c['triangles'])
                    count += 1
        self.assertEqual(count,21)

    def test_tampering_is_rejected_and_unknown_paths_are_not_served(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            data=b'original'
            (root/'file.json').write_bytes(b'changed')
            (root/'asset-manifest.json').write_text(json.dumps([{'url':'/rack-references/file.json','file':'file.json','mime':'application/json','sha256':hashlib.sha256(data).hexdigest()}]),encoding='utf-8')
            with patch.object(rack_references,'ROOT',root):
                with self.assertRaisesRegex(ValueError,'integrity'):
                    rack_references.asset('/rack-references/file.json')
                self.assertIsNone(rack_references.asset('/rack-references/../app.py'))
                self.assertIsNone(rack_references.asset('/rack-references/asset-manifest.json'))

    def test_reference_route_never_accesses_hardware_store(self):
        class ForbiddenStore:
            def __getattribute__(self,name):
                raise AssertionError('Reference request touched hardware: '+name)
        handler_type=make_handler(ForbiddenStore(),'test-token')
        for path, expected in [('/rack-references/catalog.json',200),('/rack-references/reference_0.webp',200),('/rack-references/no-such-file',404),('/rack-reference.js',200)]:
            handler=handler_type.__new__(handler_type)
            handler.path=path
            handler.valid_host=lambda:True
            responses=[]
            handler.send=lambda value,status=200,mime='application/json':responses.append((value,status,mime))
            handler.do_GET()
            self.assertEqual(responses[0][1],expected)
            self.assertTrue(responses[0][0])

    def test_served_page_scripts_match_the_manifest(self):
        # Editing rack-layout.js / rack-studio.js etc. without updating asset-manifest.json makes the server refuse the
        # script (409) and the page silently loses it; catch that here instead of in the browser.
        for entry in json.loads((rack_references.ROOT / 'asset-manifest.json').read_text(encoding='utf-8')):
            if entry['file'].endswith('.js'):
                with self.subTest(entry['file']):
                    self.assertIsNotNone(rack_references.asset(entry['url']))


if __name__ == '__main__':
    unittest.main()
