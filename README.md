# sensor-data-backend

A lightweight Python backend that accepts sensor data.

## Run locally with Docker

Build the image:

```bash
docker build -t sensor-data-backend .
```

Run it:

```bash
docker run --rm -p 8000:8000 -v "$(pwd)/database.db:/app/database.db" sensor-data-backend
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

The SQLite database file `database.db` is located in the project folder.
To view all the stored sensor data records:

```bash
sqlite3 database.db "SELECT * FROM sensor_data_records;"
```
