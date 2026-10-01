from flask import Flask, jsonify
import random
from datetime import datetime
import threading
import time
import os

app = Flask(__name__)

latest_reading = {
    "heartRate": 75,
    "oxygenLevel": 98,
    "temperature": 98.2,
    "timestamp": datetime.now().strftime("%H:%M:%S")
}


def update_reading_loop():
    global latest_reading

    while True:
        latest_reading = {
            "heartRate": random.randint(65, 105),
            "oxygenLevel": random.randint(94, 100),
            "temperature": round(random.uniform(97.0, 99.5), 1),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        time.sleep(1)


@app.route("/")
def dashboard():
    return r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>MedDeviceMonitor | Live Medical Telemetry</title>

    <style>
        * {
            box-sizing: border-box;
        }

        :root {
            --bg: #071018;
            --panel: #0c1721;
            --panel-light: #101e2a;
            --border: #1d3443;
            --text: #edf7fb;
            --muted: #78909f;
            --cyan: #00d9ff;
            --green: #35e08d;
            --yellow: #f7c948;
            --red: #ff5f6d;
        }

        body {
            margin: 0;
            min-height: 100vh;
            background:
                radial-gradient(circle at 85% 0%, rgba(0, 217, 255, 0.08), transparent 30%),
                var(--bg);
            color: var(--text);
            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }

        .shell {
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px;
        }

        header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 24px;
            margin-bottom: 28px;
        }

        .eyebrow {
            color: var(--cyan);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        h1 {
            margin: 0;
            font-size: clamp(30px, 4vw, 48px);
            letter-spacing: -0.04em;
        }

        .subtitle {
            margin-top: 8px;
            color: var(--muted);
            font-size: 15px;
        }

        .connection {
            display: flex;
            align-items: center;
            gap: 10px;
            border: 1px solid var(--border);
            background: var(--panel);
            border-radius: 999px;
            padding: 10px 15px;
            color: var(--green);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.08em;
            white-space: nowrap;
        }

        .dot {
            width: 9px;
            height: 9px;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 12px var(--green);
        }

        .metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 18px;
            margin-bottom: 18px;
        }

        .metric-card,
        .panel {
            border: 1px solid var(--border);
            background: linear-gradient(145deg, var(--panel-light), var(--panel));
            border-radius: 18px;
        }

        .metric-card {
            padding: 22px;
            min-height: 170px;
            position: relative;
            overflow: hidden;
        }

        .metric-card::after {
            content: "";
            position: absolute;
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: rgba(0, 217, 255, 0.04);
            right: -40px;
            bottom: -50px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 12px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-weight: 700;
        }

        .metric-row {
            display: flex;
            align-items: baseline;
            gap: 9px;
            margin-top: 18px;
        }

        .metric-value {
            font-size: clamp(38px, 5vw, 58px);
            font-weight: 700;
            letter-spacing: -0.05em;
        }

        .metric-unit {
            color: var(--muted);
            font-size: 16px;
        }

        .status {
            display: inline-block;
            margin-top: 12px;
            padding: 5px 9px;
            border-radius: 6px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.1em;
        }

        .status.normal {
            background: rgba(53, 224, 141, 0.1);
            color: var(--green);
        }

        .status.warning {
            background: rgba(247, 201, 72, 0.1);
            color: var(--yellow);
        }

        .status.critical {
            background: rgba(255, 95, 109, 0.1);
            color: var(--red);
        }

        .chart-panel {
            padding: 22px;
            margin-bottom: 18px;
        }

        .panel-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            margin-bottom: 18px;
        }

        .panel-title {
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }

        .live-label {
            color: var(--green);
            font-size: 11px;
            font-weight: 700;
        }

        .chart-grid {
            display: grid;
            grid-template-columns: 90px 1fr;
            align-items: center;
            gap: 12px;
            margin: 12px 0;
        }

        .chart-label {
            color: var(--muted);
            font-size: 12px;
        }

        .chart {
            height: 80px;
            width: 100%;
            background: #08121a;
            border: 1px solid #162a37;
            border-radius: 10px;
            overflow: hidden;
        }

        svg {
            width: 100%;
            height: 100%;
            display: block;
        }

        .grid-line {
            stroke: #122531;
            stroke-width: 1;
        }

        .trace {
            fill: none;
            stroke: var(--cyan);
            stroke-width: 2;
            vector-effect: non-scaling-stroke;
        }

        .trace.o2 {
            stroke: var(--green);
        }

        .trace.temp {
            stroke: var(--yellow);
        }

        .lower-grid {
            display: grid;
            grid-template-columns: 1fr 1.3fr;
            gap: 18px;
        }

        .panel {
            padding: 22px;
        }

        .info-row {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            padding: 12px 0;
            border-bottom: 1px solid #172a36;
            font-size: 13px;
        }

        .info-row:last-child {
            border-bottom: 0;
        }

        .info-label {
            color: var(--muted);
        }

        .healthy {
            color: var(--green);
            font-weight: 700;
        }

        .events {
            max-height: 270px;
            overflow-y: auto;
        }

        .event {
            display: grid;
            grid-template-columns: 72px 1fr auto;
            gap: 12px;
            align-items: center;
            padding: 11px 0;
            border-bottom: 1px solid #172a36;
            font-size: 12px;
        }

        .event-time {
            color: var(--muted);
            font-variant-numeric: tabular-nums;
        }

        .event-type {
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.08em;
            color: var(--green);
        }

        .system-bar {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
            margin-top: 18px;
        }

        .system-item {
            border: 1px solid var(--border);
            background: var(--panel);
            border-radius: 12px;
            padding: 14px;
        }

        .system-name {
            color: var(--muted);
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .system-value {
            margin-top: 6px;
            font-size: 12px;
            font-weight: 700;
            color: var(--green);
        }

        footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            color: var(--muted);
            font-size: 11px;
            margin-top: 20px;
            padding: 0 3px;
        }

        code {
            color: var(--cyan);
        }

        @media (max-width: 900px) {
            .metrics,
            .lower-grid {
                grid-template-columns: 1fr;
            }

            .system-bar {
                grid-template-columns: repeat(2, 1fr);
            }

            header {
                flex-direction: column;
            }
        }

        @media (max-width: 600px) {
            .shell {
                padding: 20px 14px;
            }

            .chart-grid {
                grid-template-columns: 1fr;
            }

            .system-bar {
                grid-template-columns: 1fr;
            }

            footer {
                flex-direction: column;
                align-items: flex-start;
            }
        }
    </style>
</head>

<body>

<div class="shell">

    <header>
        <div>
            <div class="eyebrow">Medical Device Telemetry Platform</div>
            <h1>MedDeviceMonitor</h1>
            <div class="subtitle">
                Real-time simulated patient telemetry · AWS cloud deployment
            </div>
        </div>

        <div class="connection">
            <span class="dot"></span>
            DEVICE ONLINE
        </div>
    </header>


    <section class="metrics">

        <div class="metric-card">
            <div class="metric-label">Heart Rate</div>

            <div class="metric-row">
                <div id="hr" class="metric-value">--</div>
                <div class="metric-unit">BPM</div>
            </div>

            <span id="hrStatus" class="status normal">NORMAL</span>
        </div>


        <div class="metric-card">
            <div class="metric-label">Blood Oxygen</div>

            <div class="metric-row">
                <div id="o2" class="metric-value">--</div>
                <div class="metric-unit">%</div>
            </div>

            <span id="o2Status" class="status normal">NORMAL</span>
        </div>


        <div class="metric-card">
            <div class="metric-label">Temperature</div>

            <div class="metric-row">
                <div id="temp" class="metric-value">--</div>
                <div class="metric-unit">°F</div>
            </div>

            <span id="tempStatus" class="status normal">NORMAL</span>
        </div>

    </section>


    <section class="panel chart-panel">

        <div class="panel-title-row">
            <div class="panel-title">Live Telemetry</div>
            <div class="live-label">● STREAMING</div>
        </div>


        <div class="chart-grid">
            <div class="chart-label">Heart Rate</div>

            <div class="chart">
                <svg viewBox="0 0 800 80" preserveAspectRatio="none">
                    <line class="grid-line" x1="0" y1="40" x2="800" y2="40"></line>
                    <polyline id="hrTrace" class="trace" points=""></polyline>
                </svg>
            </div>
        </div>


        <div class="chart-grid">
            <div class="chart-label">SpO₂</div>

            <div class="chart">
                <svg viewBox="0 0 800 80" preserveAspectRatio="none">
                    <line class="grid-line" x1="0" y1="40" x2="800" y2="40"></line>
                    <polyline id="o2Trace" class="trace o2" points=""></polyline>
                </svg>
            </div>
        </div>


        <div class="chart-grid">
            <div class="chart-label">Temperature</div>

            <div class="chart">
                <svg viewBox="0 0 800 80" preserveAspectRatio="none">
                    <line class="grid-line" x1="0" y1="40" x2="800" y2="40"></line>
                    <polyline id="tempTrace" class="trace temp" points=""></polyline>
                </svg>
            </div>
        </div>

    </section>


    <div class="lower-grid">

        <section class="panel">

            <div class="panel-title-row">
                <div class="panel-title">Device Status</div>
                <div class="live-label">CONNECTED</div>
            </div>

            <div class="info-row">
                <span class="info-label">Device ID</span>
                <span>MDM-SIM-001</span>
            </div>

            <div class="info-row">
                <span class="info-label">Device Type</span>
                <span>Multi-Parameter Monitor</span>
            </div>

            <div class="info-row">
                <span class="info-label">Connection</span>
                <span class="healthy">● ACTIVE</span>
            </div>

            <div class="info-row">
                <span class="info-label">REST API</span>
                <span class="healthy">● HEALTHY</span>
            </div>

            <div class="info-row">
                <span class="info-label">Last Reading</span>
                <span id="time">--</span>
            </div>

            <div class="info-row">
                <span class="info-label">Update Frequency</span>
                <span>1 second</span>
            </div>

        </section>


        <section class="panel">

            <div class="panel-title-row">
                <div class="panel-title">Recent Telemetry Events</div>
                <div class="live-label">LIVE</div>
            </div>

            <div id="events" class="events">
                <div class="event">
                    <span class="event-time">--:--:--</span>
                    <span>Waiting for telemetry...</span>
                    <span class="event-type">SYSTEM</span>
                </div>
            </div>

        </section>

    </div>


    <section class="system-bar">

        <div class="system-item">
            <div class="system-name">AWS EC2</div>
            <div class="system-value">● ONLINE</div>
        </div>

        <div class="system-item">
            <div class="system-name">Flask API</div>
            <div class="system-value">● HEALTHY</div>
        </div>

        <div class="system-item">
            <div class="system-name">Gunicorn</div>
            <div class="system-value">● RUNNING</div>
        </div>

        <div class="system-item">
            <div class="system-name">HTTPS</div>
            <div class="system-value">● SECURE</div>
        </div>

        <div class="system-item">
            <div class="system-name">CI/CD</div>
            <div class="system-value">● ACTIVE</div>
        </div>

    </section>


    <footer>
        <span>
            Simulated medical telemetry for software demonstration purposes only.
            Not intended for clinical use.
        </span>

        <span>
            REST API: <code>/api/reading</code>
        </span>
    </footer>

</div>


<script>
    const maxPoints = 50;

    const history = {
        hr: [],
        o2: [],
        temp: []
    };

    let previousState = {
        hr: null,
        o2: null,
        temp: null
    };


    function getHeartRateStatus(value) {
        if (value > 100) {
            return ["HIGH", "warning"];
        }

        return ["NORMAL", "normal"];
    }


    function getOxygenStatus(value) {
        if (value < 95) {
            return ["LOW", "critical"];
        }

        return ["NORMAL", "normal"];
    }


    function getTemperatureStatus(value) {
        if (value > 99.0) {
            return ["ELEVATED", "warning"];
        }

        return ["NORMAL", "normal"];
    }


    function setStatus(elementId, status) {
        const element = document.getElementById(elementId);

        element.textContent = status[0];
        element.className = "status " + status[1];
    }


    function addPoint(array, value) {
        array.push(value);

        if (array.length > maxPoints) {
            array.shift();
        }
    }


    function renderTrace(elementId, values, min, max) {
        if (values.length < 2) {
            return;
        }

        const width = 800;
        const height = 80;

        const points = values.map((value, index) => {
            const x = (index / (maxPoints - 1)) * width;

            const normalized = Math.max(
                0,
                Math.min(1, (value - min) / (max - min))
            );

            const y = height - (normalized * height);

            return x.toFixed(1) + "," + y.toFixed(1);
        });

        document
            .getElementById(elementId)
            .setAttribute("points", points.join(" "));
    }


    function addEvent(time, message, type, colorClass = "") {
        const events = document.getElementById("events");

        const event = document.createElement("div");
        event.className = "event";

        event.innerHTML =
            '<span class="event-time">' + time + '</span>' +
            '<span>' + message + '</span>' +
            '<span class="event-type ' + colorClass + '">' + type + '</span>';

        events.prepend(event);

        while (events.children.length > 8) {
            events.removeChild(events.lastChild);
        }
    }


    function evaluateEvents(data, statuses) {
        const states = {
            hr: statuses.hr[0],
            o2: statuses.o2[0],
            temp: statuses.temp[0]
        };

        if (previousState.hr !== states.hr) {
            addEvent(
                data.timestamp,
                states.hr === "NORMAL"
                    ? "Heart rate returned to normal range"
                    : "Elevated heart rate detected",
                states.hr
            );
        }

        if (previousState.o2 !== states.o2) {
            addEvent(
                data.timestamp,
                states.o2 === "NORMAL"
                    ? "Blood oxygen within normal range"
                    : "Low blood oxygen detected",
                states.o2
            );
        }

        if (previousState.temp !== states.temp) {
            addEvent(
                data.timestamp,
                states.temp === "NORMAL"
                    ? "Temperature within normal range"
                    : "Elevated temperature detected",
                states.temp
            );
        }

        previousState = states;
    }


    async function updateReading() {
        try {
            const response = await fetch("/api/reading", {
                cache: "no-store"
            });

            if (!response.ok) {
                throw new Error("API request failed");
            }

            const data = await response.json();

            document.getElementById("hr").textContent = data.heartRate;
            document.getElementById("o2").textContent = data.oxygenLevel;
            document.getElementById("temp").textContent = data.temperature;
            document.getElementById("time").textContent = data.timestamp;

            const statuses = {
                hr: getHeartRateStatus(data.heartRate),
                o2: getOxygenStatus(data.oxygenLevel),
                temp: getTemperatureStatus(data.temperature)
            };

            setStatus("hrStatus", statuses.hr);
            setStatus("o2Status", statuses.o2);
            setStatus("tempStatus", statuses.temp);

            addPoint(history.hr, data.heartRate);
            addPoint(history.o2, data.oxygenLevel);
            addPoint(history.temp, data.temperature);

            renderTrace("hrTrace", history.hr, 55, 115);
            renderTrace("o2Trace", history.o2, 90, 100);
            renderTrace("tempTrace", history.temp, 96, 101);

            evaluateEvents(data, statuses);

        } catch (error) {
            console.error("Telemetry update failed:", error);
        }
    }


    updateReading();
    setInterval(updateReading, 1000);
</script>

</body>
</html>
    """


@app.route("/api/reading")
def api_reading():
    return jsonify(latest_reading)


@app.route("/raw")
def raw_reading():
    return (
        f"HR:{latest_reading['heartRate']},"
        f"O2:{latest_reading['oxygenLevel']},"
        f"TEMP:{latest_reading['temperature']}"
    )


# Start the simulated medical-device data generator.
# This runs when the application is loaded by Gunicorn or started directly.
thread = threading.Thread(target=update_reading_loop, daemon=True)
thread.start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)