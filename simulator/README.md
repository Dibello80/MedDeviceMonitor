# Medical Device Simulator (Flask)

This module simulates a medical device that generates real-time vital signs and exposes them via an HTTP API.

It is intended for local development and testing of the Kotlin monitoring application.

---

## Overview

The simulator mimics a physical medical sensor by producing randomized readings every second:

* Heart Rate (BPM)
* Oxygen Level (%)
* Temperature (°F)

Data is accessible through REST endpoints and a simple web dashboard.

---

## Endpoints

### `GET /api/reading`

Returns the latest reading in JSON format.

Example:

```json
{
  "heartRate": 82,
  "oxygenLevel": 97,
  "temperature": 98.3,
  "timestamp": "14:32:10"
}
```

---

### `GET /raw`

Returns a compact string format:

```text
HR:82,O2:97,TEMP:98.3
```

---

### `GET /`

Web dashboard for quick visualization of live data.

---

## How It Works

* A background thread updates simulated readings every second
* Values are randomized within realistic ranges
* The latest reading is stored in memory and served via API

---

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

## Requirements

```text
Flask==3.0.3
```

---

## Notes

* This is a **simulation only** (no real sensor data)
* Designed for integration testing with the Android app
* Not intended for production or medical use

---

## Future Improvements

* BLE (Bluetooth Low Energy) broadcasting
* Configurable ranges and thresholds
* Simulated connection drops / faults
* Device ID and authentication layer

