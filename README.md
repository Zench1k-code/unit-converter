# Unit converter

## What it does

A tiny HTTP service that converts between units of length (m, km, mi, ft),
mass (kg, g, lb) and temperature (c, f, k). Standard library only.

## Run

    scripts/run.sh

Listens on `$PORT` (default **8080**). Example:

    curl "localhost:8080/convert?value=10&from=km&to=mi"

## Endpoints

- `GET /healthz` returns 200 `{"status": "ok"}`
- `GET /convert?value=..&from=..&to=..` returns the converted value

## Configuration

- `PORT` - the port to listen on (default 8080)
- `GREETING` - text returned by `GET /` (default `hello`)
- `API_KEY` - a secret; `GET /` only reports whether it is set, never its value

## Test

    scripts/test.sh

Prints `TESTS: n/n` and exits 0 when everything passes.

## Examples

    curl "localhost:8080/convert?value=100&from=c&to=f"
    curl "localhost:8080/convert?value=1&from=kg&to=lb"