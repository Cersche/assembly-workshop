"""Export integrity/provenance checks with synthetic geometry only; no creator export."""
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import rack_references
import rack_stl


class RackStlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mesh = {'vertices': [[0, 0, 0], [1, 0, 0], [0, 1, 0]], 'triangles': [[0, 1, 2]]}
        self.catalog = {'references': [{'id': '0', 'source_file': 'synthetic.3mf',
            'source_sha256': 'synthetic-source-hash', 'license_metadata': 'synthetic license',
            'components': [{'id': '1', 'name': 'Synthetic.stl', 'unit': 'millimeter',
                'source_member': '3D/test.model', 'url': '/rack-references/component_0_1.json'}]}]}
        entries = []
        for name, value in [('catalog.json', self.catalog), ('component_0_1.json', self.mesh)]:
            data = json.dumps(value).encode('utf-8')
            (self.root / name).write_bytes(data)
            entries.append({'url': '/rack-references/' + name, 'file': name,
                'mime': 'application/json', 'sha256': rack_references.digest(data, 'application/json')})
        (self.root / 'asset-manifest.json').write_text(json.dumps(entries), encoding='utf-8')
        self.patcher = patch.object(rack_references, 'ROOT', self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.part = {'ref': 0, 'id': '1', 'count': 4}

    def export(self, parts=None):
        return rack_stl.export({'rack': 'Synthetic rack', 'parts': parts or [self.part]})

    def test_archive_records_exact_source_and_stl_identity_and_quantity(self):
        with zipfile.ZipFile(io.BytesIO(self.export())) as archive:
            stl = archive.read('4x Synthetic.stl')
            record = json.loads(archive.read('source-manifest.json'))['parts'][0]
            self.assertEqual(record['source_sha256'], 'synthetic-source-hash')
            self.assertEqual(record['license_metadata'], 'synthetic license')
            self.assertEqual(record['source_member'], '3D/test.model')
            self.assertEqual(record['object_id'], '1')
            self.assertEqual(record['count'], 4)
            self.assertEqual(record['stl_sha256'], hashlib.sha256(stl).hexdigest())
            self.assertEqual(record['unit'], 'millimeter')
            self.assertEqual(struct.unpack_from('<9f', stl, 96), tuple(sum(self.mesh['vertices'], [])))
            self.assertIn(b'UNKNOWN', archive.read('parts-list.txt'))

    def test_mesh_or_catalog_tampering_blocks_export(self):
        for name in ('component_0_1.json', 'catalog.json'):
            path = self.root / name
            before = path.read_bytes()
            path.write_bytes(b'{}')
            with self.assertRaisesRegex(ValueError, 'integrity'):
                self.export()
            path.write_bytes(before)

    def test_unknown_negative_traversal_and_duplicate_references_rejected(self):
        for parts in ([{**self.part, 'ref': -1}], [{**self.part, 'ref': '../0'}],
                      [{**self.part, 'id': 'no-such-id'}], [self.part, self.part], ['invalid']):
            with self.subTest(parts=parts), self.assertRaises(ValueError):
                self.export(parts)

    def test_invalid_counts_rejected(self):
        for count in (0, -1, 201, True, 1.5, '4', None):
            with self.subTest(count=count), self.assertRaises(ValueError):
                self.export([{**self.part, 'count': count}])

    def test_unlisted_component_blocks_export(self):
        (self.root / 'component_0_1.json').unlink()
        with patch.object(rack_references, 'asset', side_effect=lambda url:
                (json.dumps(self.catalog).encode('utf-8'), 'application/json') if url.endswith('catalog.json') else None):
            with self.assertRaisesRegex(ValueError, 'Unknown rack source'):
                self.export()


if __name__ == '__main__':
    unittest.main()
