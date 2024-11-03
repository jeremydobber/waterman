"""Data models."""

from . import db

"""Table for the downloaded data"""
class Precipitation(db.Model):
    __tablename__ = "precipitation"
    time = db.Column(db.DateTime, primary_key=True)
    pr = db.Column(db.Float, index=False, unique=False, nullable=True)

"""Table for the observed storage state"""
class ObsAvailable(db.Model):
    __tablename__ = "obs_available"
    time = db.Column(db.DateTime, primary_key=True)
    pr = db.Column(db.Float, index=False, unique=False, nullable=True)

"""Table for the observed consumption"""
class ObsConsumption(db.Model):
    __tablename__ = "obs_consumption"
    time = db.Column(db.DateTime, primary_key=True)
    pr = db.Column(db.Float, index=False, unique=False, nullable=True)

"""Table for the settings ???"""
class Config(db.Model):
    __tablename__ = "config"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True, nullable=False)
    setup_complete = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    location_name = db.Column(db.String, index=False, unique=False, nullable=True)
    location_lat = db.Column(db.Float, index=False, unique=False, nullable=True)
    location_lon = db.Column(db.Float, index=False, unique=False, nullable=True)
    storage_size = db.Column(db.Float, index=False, unique=False, nullable=True)
    roof_size = db.Column(db.Float, index=False, unique=False, nullable=True)
    people = db.Column(db.Integer, index=False, unique=False, nullable=True)

    def __repr__(self):
        return "<Settings {}>".format(self.location_name)

# class User(db.Model):
#     """Data model for user accounts."""

#     __tablename__ = "flasksqlalchemy-tutorial-users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=False, unique=True, nullable=False)
#     email = db.Column(db.String(80), index=True, unique=True, nullable=False)
#     created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
#     bio = db.Column(db.Text, index=False, unique=False, nullable=True)
#     admin = db.Column(db.Boolean, index=False, unique=False, nullable=False)

#     def __repr__(self):
#         return "<User {}>".format(self.username)
