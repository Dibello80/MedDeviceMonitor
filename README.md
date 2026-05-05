## Demo

Real-time Android medical monitoring app connected to an external device server.

- Live data streaming
- Alert detection
- Smooth chart visualization

# MedDeviceMonitor

Android medical device monitoring app built with Kotlin and Jetpack Compose.

## Features

- Real-time vital monitoring (Heart Rate, Oxygen, Temperature)
- External device integration via HTTP (simulated medical device server)
- MVVM architecture with StateFlow
- Live animated chart visualization
- Alert detection (abnormal readings)
- Device connection state (Connecting / Connected / Disconnected)
- Event logging system

## Tech Stack

- Kotlin
- Jetpack Compose
- MVVM Architecture
- StateFlow
- Coroutines
- Canvas (custom chart rendering)
- Flask (device simulation server)

## How It Works

The app connects to an external device server:

Example data: HR:82,O2:97,TEMP:98.4


## Screenshots

### Device Server (Simulated Sensor)
![Server](screenshots/server_dashboard.png)

### Android App Dashboard
![Dashboard](screenshots/app_dashboard.png)

### Normal Monitoring State
![Normal](screenshots/app_normal.png)

### Alert State (Abnormal Readings)
![Alert](screenshots/app_alert.png)

## Future Improvements

- Bluetooth BLE device integration
- ESP32 real hardware support
- Advanced charting (multi-signal ECG style)
- Data persistence and history tracking

## Author

Angelo R. Dibello
