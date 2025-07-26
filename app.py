from flask import Flask, jsonify, request, send_from_directory
import Adafruit_DHT, RPi.GPIO as GPIO, sqlite3, os
from flask_cors import CORS
from twilio.rest import Client
import paho.mqtt.client as mqtt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
jwt = JWTManager(app)

GPIO.setmode(GPIO.BCM)
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

conn = sqlite3.connect('data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS readings (time TEXT, temperature REAL, humidity REAL)")
conn.commit()

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

@app.route("/login", methods=['POST'])
def login():
    if request.json.get('username') == 'admin' and request.json.get('password') == 'raspberry':
        token = create_access_token(identity='admin')
        return jsonify(access_token=token)
    return jsonify({"msg": "Bad username/password"}), 401

@app.route("/temperature")
@jwt_required()
def read_temp():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity and temperature:
        cursor.execute("INSERT INTO readings VALUES (datetime('now'), ?, ?)", (temperature, humidity))
        conn.commit()
        client.publish("iot/temperature", f"Temp:{temperature},Humidity:{humidity}")
        if temperature > 30:
            twilio_client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_AUTH'))
            twilio_client.messages.create(
                to=os.getenv('TWILIO_TO'),
                from_=os.getenv('TWILIO_FROM'),
                body=f"ALERT! High Temperature Detected: {temperature} °C"
            )
        return jsonify({"temperature": temperature, "humidity": humidity})
    return jsonify({"error": "Sensor read failure"})

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
