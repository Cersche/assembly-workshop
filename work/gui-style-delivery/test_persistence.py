"""Focused stylesheet regression checks; isolated fixtures only."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

APP = Path(__file__).resolve().parents[2] / 'outputs/Mechanical_Design_App'
sys.path.insert(0, str(APP))
import app


class DeliveryTests(unittest.TestCase):
    def root(self, path='/'):
        class NoStore:
            def __getattribute__(self, name):
                raise AssertionError('Document delivery accessed data: ' + name)
        cls = app.make_handler(NoStore(), 'fixture-token')
        handler = cls.__new__(cls)
        handler.path = path
        handler.valid_host = lambda: True
        result = []
        handler.send = lambda value, status=200, mime='application/json': result.append((value, status, mime))
        handler.do_GET()
        return result[0]

    def test_twenty_repeated_document_loads(self):
        css = (APP / 'workspace.css').read_text(encoding='utf-8')
        for i in range(20):
            with self.subTest(load=i):
                html, status, mime = self.root('/?reload=' + str(i))
                self.assertEqual((status, mime), (200, 'text/html'))
                self.assertEqual(html.count('<style id="studio-workspace-css">'), 1)
                self.assertIn('<style id="studio-workspace-css">' + css + '</style>', html)
                self.assertNotIn('<link rel="stylesheet" href="/workspace.css', html)
                self.assertIn("const token='fixture-token'", html)

    def test_css_is_read_fresh_without_restart(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent, prefix='css-fixture-') as folder:
            root = Path(folder)
            (root / 'index.html').write_text((APP / 'index.html').read_text(encoding='utf-8'), encoding='utf-8')
            with patch.object(app, 'ROOT', root):
                for color in ('#123456', '#abcdef'):
                    css = '/* café */ body{color:' + color + '}'
                    (root / 'workspace.css').write_text(css, encoding='utf-8')
                    self.assertIn('<style id="studio-workspace-css">' + css + '</style>', self.root()[0])

    def test_missing_css_does_not_serve_unstyled_success(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent, prefix='missing-css-') as folder:
            root = Path(folder)
            (root / 'index.html').write_text((APP / 'index.html').read_text(encoding='utf-8'), encoding='utf-8')
            with patch.object(app, 'ROOT', root):
                self.assertEqual(self.root()[1], 400)


if __name__ == '__main__':
    unittest.main(verbosity=2)
