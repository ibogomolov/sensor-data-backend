# sensor-data-backend

A lightweight Python backend that accepts sensor data.

## Run locally with Docker

Build the image:

```bash
docker build -t sensor-data-backend .
```

Run it:

```bash
docker run --rm -p 8000:8000 -v "$(pwd):/app/external_volume/" sensor-data-backend
```

The API is served at `http://127.0.0.1:8000`.
Sample request:

```bash
curl -X POST --location "http://127.0.0.1:8000/sensor_data" \
    -H "Content-Type: application/json" \
    -d '{
          "asset_id": "WTG-Offshore-01",
          "timestamp": "2026-02-15T10:30:00Z",
          "sensors": {
            "vibration_x": 0.05,
            "strain_gauge_1": 450.2,
            "temperature": 65.0
          }
        }'
```

## Access the DB

The SQLite database file `database.db` will be located in the project folder, after the first run of the application.
To view all the stored sensor data records:

```bash
sqlite3 database.db "SELECT * FROM sensor_data_records;"
```

## Metrics

The application contains the metrics middleware to collect and report service performance metrics in the standard Prometheus text format:

- `http_requests_total` — request count by `status_code`, for success/failure rates and overall throughput.
- `http_request_duration_seconds` — request latency histogram, for latency  quantiles (p50, p95, p99).

```bash
curl http://127.0.0.1:8000/metrics
```
