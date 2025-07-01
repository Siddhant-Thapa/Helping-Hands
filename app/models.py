from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(50), nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)


class Branch(db.Model):
    __tablename__ = 'branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(50), default='Bangalore')

    slots = db.relationship('Slot', backref='branch', lazy=True)


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # E.g., 'Veg', 'Non-Veg', etc.

    slots = db.relationship('Slot', backref='section', lazy=True)


class Slot(db.Model):
    __tablename__ = 'slots'
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey(
        'branches.id'), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'sections.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    bookings = db.relationship('Booking', backref='slot', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # e.g., 'booked', 'cancelled'
    status = db.Column(db.String(20), default='booked')

    feedback = db.relationship('Feedback', backref='booking', uselist=False)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey(
        'bookings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
