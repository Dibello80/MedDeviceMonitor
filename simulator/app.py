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
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fake Medical Device Server</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0D1117;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }
            .dashboard {
                width: 420px;
                background: #161B22;
                padding: 28px;
                border-radius: 22px;
                box-shadow: 0 0 30px rgba(0, 229, 255, 0.15);
            }
            h1 { margin-top: 0; color: #00E5FF; }
            .subtitle { color: #8B949E; margin-bottom: 24px; }
            .card {
                background: #0D1117;
                border-radius: 18px;
                padding: 18px;
                margin-bottom: 14px;
                border: 1px solid #30363D;
            }
            .label { color: #8B949E; font-size: 14px; }
            .value {
                font-size: 34px;
                font-weight: bold;
                margin-top: 6px;
            }
            .ok { color: #2ECC71; }
            .warn { color: #FF5252; }
            .footer {
                margin-top: 20px;
                color: #8B949E;
                font-size: 13px;
            }
        </style>
    </head>
    <body>
        <div class="dashboard">
            <h1>MedDevice Server</h1>
            <div class="subtitle">Simulated external medical sensor</div>

            <div class="card">
                <div class="label">Heart Rate</div>
                <div id="hr" class="value">-- bpm</div>
            </div>

            <div class="card">
                <div class="label">Oxygen Level</div>
                <div id="o2" class="value">-- %</div>
            </div>

            <div class="card">
                <div class="label">Temperature</div>
                <div id="temp" class="value">-- °F</div>
            </div>

            <div class="footer">
                Last update: <span id="time">--</span><br>
                API endpoint: /api/reading
            </div>
        </div>

        <script>
            async function updateReading() {
                const response = await fetch('/api/reading');
                const data = await response.json();

                document.getElementById('hr').textContent = data.heartRate + ' bpm';
                document.getElementById('o2').textContent = data.oxygenLevel + ' %';
                document.getElementById('temp').textContent = data.temperature + ' °F';
                document.getElementById('time').textContent = data.timestamp;

                document.getElementById('hr').className =
                    data.heartRate > 100 ? 'value warn' : 'value ok';

                document.getElementById('o2').className =
                    data.oxygenLevel < 95 ? 'value warn' : 'value ok';

                document.getElementById('temp').className =
                    data.temperature > 99.0 ? 'value warn' : 'value ok';
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
    return f"HR:{latest_reading['heartRate']},O2:{latest_reading['oxygenLevel']},TEMP:{latest_reading['temperature']}"

if __name__ == "__main__":
    thread = threading.Thread(target=update_reading_loop, daemon=True)
    thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)