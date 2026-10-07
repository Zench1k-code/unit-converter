import json
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import app  # noqa: E402  (fails if the application is deleted -> tests go red)


class ConvertFunction(unittest.TestCase):
    def test_km_to_miles(self):
        self.assertAlmostEqual(app.convert(10, "km", "mi"), 6.213712, places=5)

    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(app.convert(100, "c", "f"), 213.0)

    def test_unknown_unit(self):
        with self.assertRaises(ValueError):
            app.convert(1, "km", "kg")


class HttpService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.Handler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.base + path) as r:
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            with e:
                return e.code, json.load(e)

    def test_healthz(self):
        self.assertEqual(self.get("/healthz"), (200, {"status": "ok"}))

    def test_convert_endpoint(self):
        status, body = self.get("/convert?value=1&from=kg&to=lb")
        self.assertEqual(status, 200)
        self.assertAlmostEqual(body["result"], 2.204623, places=5)

    def test_bad_request(self):
        status, _ = self.get("/convert?value=abc&from=km&to=mi")
        self.assertEqual(status, 400)


if __name__ == "__main__":
    unittest.main()
