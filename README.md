🌐 Raspberry Pi IoT Monitoring System – Full Stack with React, Python, MQTT, SQLite, Twilio & Docker

> Real-time Temperature & Humidity Monitoring Dashboard with Alerts, Authentication & Expandable Sensor Support

🚀 Project Overview

This is a production-grade IoT system that uses a React frontend and a Python Flask backend to monitor temperature and humidity sensors (e.g., DHT11/DHT22) connected to a Raspberry Pi GPIO. 

It supports:

- Real-time data visualization
- JWT-based authentication
- Data storage in SQLite
- MQTT-based Pub/Sub architecture
- Alerting via Twilio SMS
- Deployment with Docker & Nginx

🖼️ System Architecture

┌────────────┐      MQTT       ┌─────────────┐
│  Sensors   │ ─────────────▶ │   Flask API │
└────────────┘                └────┬────────┘
│ REST
┌─────▼──────┐
│  React.js  │
└─────┬──────┘
│
┌─────▼─────┐
│ SQLite DB │
└───────────┘
│
┌─────▼─────┐
│  Twilio   │ (Alerting)
└───────────┘

🧰 Tech Stack

- Frontend: React.js + `recharts` for live graphs
- Backend: Python Flask + `paho-mqtt` + `sqlite3`
- Authentication: JWT tokens (`pyjwt`)
- Database: SQLite (can be replaced with PostgreSQL)
- Sensor Interface: Raspberry Pi GPIO (e.g., DHT11)
- Messaging: MQTT (via `paho-mqtt`)
- Alerting: Twilio SMS (via `twilio` package)
- Deployment: Docker + Docker Compose + Nginx

🔌 Hardware Requirements

- Raspberry Pi (any modern version)
- DHT11 or DHT22 Sensor (or any GPIO-based temp/humidity sensor)
- Jumper wires
- Breadboard (optional)

🔧 Installation

📁 Clone Repository

bash
git clone https://github.com/your-username/raspberry-pi-iot-monitor.git
cd raspberry-pi-iot-monitor

🐳 Run with Docker Compose

bash
docker-compose up --build

 🔐 Authentication

* Use `/login` endpoint with hardcoded credentials to get JWT token.
* Pass token as `Authorization: Bearer <token>` for protected routes.

📡 MQTT Setup

The backend subscribes to `sensor/temperature` and `sensor/humidity`.

To publish test data:

bash
mosquitto_pub -h localhost -t sensor/temperature -m "31.2"
mosquitto_pub -h localhost -t sensor/humidity -m "65.5"


📈 Frontend Preview

* Runs on `http://localhost:3000`
* Auto-refreshes graph every 3 seconds
* Login page → token → protected dashboard
* Displays current and historical sensor data in graphs

⚠️ Alerting (Twilio SMS)

* Set thresholds in `app.py`
* If `temperature > 30`, SMS is sent to the configured number
* Configure `.env`:

env
TWILIO_SID=your_twilio_sid
TWILIO_TOKEN=your_twilio_token
TWILIO_FROM=+12012345678
TWILIO_TO=+94712345678

🛠️ Folder Structure

📦raspberry-pi-iot-monitor
 ┣ 📁backend
 ┃ ┣ 📄app.py
 ┃ ┣ 📄.env
 ┃ ┗ 📄requirements.txt
 ┣ 📁frontend
 ┃ ┣ 📄App.js
 ┃ ┣ 📄Login.js
 ┃ ┗ 📄package.json
 ┣ 📄docker-compose.yml
 ┣ 📄Dockerfile.frontend
 ┗ 📄Dockerfile.backend

🧪 Example Sensor Test Script (Python)

python
import time
import Adafruit_DHT
import paho.mqtt.publish as publish

sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    if humidity and temperature:
        publish.single("sensor/temperature", temperature, hostname="localhost")
        publish.single("sensor/humidity", humidity, hostname="localhost")
    time.sleep(3)

🔐 JWT Sample

bash
POST /login
{
  "username": "admin",
  "password": "password"
}

=> Returns token

GET /api/data (Protected)
Authorization: Bearer <your_token>

🔮 Future Extensions

* Add support for more sensor types: gas, air quality, light, etc.
* Switch from SQLite to PostgreSQL for multi-device use
* Integrate Grafana for visualization
* Expand Twilio alerts to Email (SMTP)
* Host via Kubernetes or AWS IoT
* Mobile App for remote monitoring

🤝 Contributing

Pull requests and feature suggestions are welcome. For major changes, open an issue first.

📜 License

MIT License © 💻 by L.P. Harisha Lakshan Warnakulasuriya

👨‍💻 Author & Credits

Built with 💡 and 💻 by L.P. Harisha Lakshan Warnakulasuriya

📬 For questions, projects, or consulting: unicornprofessionalbay@gmail.com

📝 License

This project is licensed under the MIT License. Use freely for educational and research purposes.