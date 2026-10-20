"""Integrity and route acceptance for the new preview renderer; no user data."""
from pathlib import Path
import hashlib
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
APP=ROOT/'outputs/Mechanical_Design_App'
sys.path.insert(0,str(APP))
import rack_references
import app

class RenderAssets(unittest.TestCase):
    def test_original_locked_asset_and_prior_manifest_entries_unchanged(self):
        expected='414214bcbf3f1f40ff7a6be0791741ec721cb3d9585cc4d148b1c68f7ff1c7d2'
        self.assertEqual(hashlib.sha256((rack_references.ROOT/'rack-scene.js').read_bytes()).hexdigest(),expected)
        before=json.loads((Path(__file__).parent/'before-app/asset-manifest.json').read_text(encoding='utf-8'))
        current=json.loads((rack_references.ROOT/'asset-manifest.json').read_text(encoding='utf-8'))
        self.assertEqual([e for e in current if e['file']!='rack-studio.js'],before)

    def test_new_asset_is_verified_and_tamper_still_rejected(self):
        original=rack_references.asset('/rack-references/rack-studio.js')
        self.assertEqual(original[0],(rack_references.ROOT/'rack-studio.js').read_bytes())
        with tempfile.TemporaryDirectory(prefix='integrity-',dir=Path(__file__).parent) as directory:
            folder=Path(directory)
            (folder/'asset-manifest.json').write_bytes((rack_references.ROOT/'asset-manifest.json').read_bytes())
            (folder/'rack-studio.js').write_bytes(original[0]+b'\n// tamper\n')
            with patch.object(rack_references,'ROOT',folder):
                with self.assertRaisesRegex(ValueError,'integrity'): rack_references.asset('/rack-references/rack-studio.js')

    def test_script_order_and_live_handler(self):
        html=(APP/'index.html').read_text(encoding='utf-8')
        self.assertLess(html.index('src="/rack-references/rack-scene.js"'),html.index('src="/rack-references/rack-studio.js"'))
        self.assertLess(html.index('src="/rack-references/rack-studio.js"'),html.index('src="/workspace.js"'))
        class Forbidden:
            def __getattribute__(self,name): raise AssertionError('Renderer route accessed user data')
        handler_type=app.make_handler(Forbidden(),'test-token')
        for url in ['/rack-references/rack-studio.js','/workspace.js']:
            handler=handler_type.__new__(handler_type);handler.path=url;handler.valid_host=lambda:True
            responses=[];handler.send=lambda value,status=200,mime='application/json':responses.append((status,mime))
            handler.do_GET();self.assertEqual(responses,[(200,'text/javascript')])

if __name__=='__main__': unittest.main(verbosity=2)
