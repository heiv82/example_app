from werkzeug.security import generate_password_hash, check_password_hash
from app import login, db
from datetime import datetime
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    api_token = db.Column(db.String(255))  #
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    devices = db.relationship('Device', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Device(db.Model):
    __tablename__ = 'devices'
    # __table_args__ = {'extend_existing': True}
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

    def __repr__(self):
        return f"<Device {self.device_name}: {self.device_EUI}>"


class DeviceData(db.Model):
    __tablename__ = 'dates'
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    device_data_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)

    def __repr__(self):
        return f"<Data: {self.message}>"


# Registration user loader in Flask - Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))