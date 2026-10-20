"""Startup burst and cancelled-response regressions; isolated data only."""
from concurrent.futures import ThreadPoolExecutor
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import threading
import unittest
from urllib.request import urlopen

HERE = Path(__file__).parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / 'outputs/Mechanical_Design_App'))
import app


class StartupTests(unittest.TestCase):
    def test_connection_burst_fits_backlog_before_accept_loop(self):
        # Establish simultaneous connections while accept is deliberately paused.
        # This reproduces the loss before request-handler logging begins.
        for cls, expected in ((app.ThreadingHTTPServer, False), (app.WorkshopHTTPServer, True)):
            with self.subTest(server=cls.__name__):
                server = cls(('127.0.0.1', 0), app.make_handler(None, 'fixture'))
                gate = threading.Barrier(24)
                def connect(_):
                    gate.wait(timeout=10)
                    try:
                        return socket.create_connection(server.server_address, timeout=0.75)
                    except OSError:
                        return None
                try:
                    with ThreadPoolExecutor(max_workers=24) as pool:
                        connections = list(pool.map(connect, range(24)))
                    accepted = sum(c is not None for c in connections)
                    print(cls.__name__, 'burst connections:', accepted, '/24', flush=True)
                    self.assertEqual(accepted == 24, expected)
                finally:
                    for connection in connections:
                        if connection:
                            connection.close()
                    server.server_close()

    def test_parallel_startup_routes(self):
        with tempfile.TemporaryDirectory(prefix='http-fixture-', dir=HERE) as folder:
            store = app.Store(Path(folder) / 'library.sqlite3')
            store.load_starter()
            base = app.make_handler(store, 'startup-test')
            class Handler(base):
                def log_message(self, *_):
                    pass
            server = app.WorkshopHTTPServer(('127.0.0.1', 0), Handler)
            worker = threading.Thread(target=server.serve_forever, kwargs={'poll_interval': 0.05}, daemon=True)
            worker.start()
            paths = ['/', '/workspace.js', '/rack-reference.js', '/viewer.js',
                     '/rack-references/rack-studio.js', '/api/state', '/api/workspace-capabilities', '/api/rack-workspace']
            def get(path):
                with urlopen('http://127.0.0.1:' + str(server.server_port) + path, timeout=10) as response:
                    return path, response.status, response.headers.get('Cache-Control'), response.read()
            try:
                for _ in range(3):
                    with ThreadPoolExecutor(max_workers=24) as pool:
                        results = list(pool.map(get, paths * 3))
                    for path, status, cache, data in results:
                        self.assertEqual(status, 200, path)
                        self.assertEqual(cache, 'no-store')
                        self.assertTrue(data)
                        if path == '/':
                            self.assertIn(b'<style id="studio-workspace-css">', data)
                print('72 parallel startup HTTP requests PASS', flush=True)
            finally:
                server.shutdown()
                worker.join(timeout=5)
                server.server_close()

    def test_cancelled_response_does_not_send_second_response(self):
        cls = app.make_handler(None, 'fixture')
        for stage in ('headers', 'body'):
            for error in (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
                with self.subTest(stage=stage, error=error.__name__):
                    handler = cls.__new__(cls)
                    sent = []
                    handler.send_response = lambda status: sent.append(status)
                    handler.send_header = lambda *args: None
                    def disconnect(*args):
                        raise error('cancelled navigation')
                    handler.end_headers = disconnect if stage == 'headers' else lambda: None
                    handler.wfile = type('Writer', (), {'write': staticmethod(disconnect)})()
                    handler.send('fixture', mime='text/javascript')
                    self.assertEqual(sent, [200])


if __name__ == '__main__':
    unittest.main(verbosity=2)
