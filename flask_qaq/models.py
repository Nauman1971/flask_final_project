from flask_login import UserMixin
from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    roles = db.Column(db.String, nullable=False)
    file = db.Column(db.LargeBinary)
    # file_name = db.Column(db.String(300))