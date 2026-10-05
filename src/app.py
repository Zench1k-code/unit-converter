"""Unit converter HTTP service (standard library only)."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

# Each category maps a unit to its size in the base unit.
FACTORS = {
    "length": {"m": 1.0, "km": 1000.0, "mi": 1609.344, "ft": 0.3048},
    "mass": {"kg": 1.0, "g": 0.001, "lb": 0.45359237},
}
TEMPERATURES = {"c", "f", "k"}


def convert(value, src, dst):
    """Convert value from unit src to unit dst. Raises ValueError on bad units."""
    src, dst = src.lower(), dst.lower()
    if src in TEMPERATURES and dst in TEMPERATURES:
        celsius = {"c": value, "f": (value - 32) * 5 / 9, "k": value - 273.15}[src]
        return {"c": celsius, "f": celsius * 9 / 5 + 32, "k": celsius + 273.15}[dst]
    for units in FACTORS.values():
        if src in units and dst in units:
            return value * units[src] / units[dst]
    raise ValueError(f"cannot convert '{src}' to '{dst}'")


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/healthz":
            return self._send(200, {"status": "ok"})
        if url.path == "/":
            return self._send(200, {"service": "unit-converter",
                                    "usage": "/convert?value=10&from=km&to=mi"})
        if url.path == "/convert":
            q = parse_qs(url.query)
            try:
                value = float(q["value"][0])
                result = convert(value, q["from"][0], q["to"][0])
            except (KeyError, IndexError):
                return self._send(400, {"error": "need value, from, to"})
            except ValueError as e:
                return self._send(400, {"error": str(e)})
            return self._send(200, {"value": value, "from": q["from"][0],
                                    "to": q["to"][0], "result": round(result, 6)})
        self._send(404, {"error": "not found"})

    def log_message(self, *args):
        pass


def main():
    port = int(os.environ.get("PORT", "8080"))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()


if __name__ == "__main__":
    main()
