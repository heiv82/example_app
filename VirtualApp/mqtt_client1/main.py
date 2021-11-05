from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import json
import base64
import paho.mqtt.client as mqtt
from datetime import datetime

app = Flask(__name__)

broker_address = "mosquitto"
app.config['SECRET_KEY'] = os.urandom(12).hex()
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:<password>@db/db_dates'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    api_token = db.Column(db.String(255))  #
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    devices = db.relationship('Device', backref='user', lazy='dynamic')


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    device_EUI = db.Column(db.String(100), index=True, unique=True)
    device_name = db.Column(db.String(100), index=True)
    description = db.Column(db.String(100), index=True)
    device_profile_id = db.Column(db.String(100), index=True)
    device_profile_name = db.Column(db.String(100), index=True)
    device_battery = db.Column(db.Integer, index=True)
    application_id = db.Column(db.String(100), index=True)
    application_name = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    device_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_data = db.relationship('DeviceData', backref='device', lazy='dynamic')


class DeviceData(db.Model):
    __tablename__ = 'dates'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    device_data_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)


db.create_all()


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("application/+/device/#")


def decode_message(message):
    encode_msg = base64.b64decode(message)
    return str(encode_msg, "utf-8")


def handle_mqtt_message(client, userdata, message):
    data = json.loads(message.payload)
    if data.get('data'):
        decode_msg = decode_message(data.get('data'))
        dev_eui = data.get('devEUI')
        device = Device.query.filter_by(device_EUI=dev_eui).first()

        device_data = DeviceData(data=decode_msg, device=device)

        try:
            db.session.add(device_data)
            db.session.commit()
        except:
            print(f"An error occurred while adding data from the device {device.device_EUI}")
    else:
        print(data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = handle_mqtt_message
client.connect(broker_address, 1883, 60)

client.loop_forever()
