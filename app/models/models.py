from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicles = db.relationship("Vehicle", backref="customer", lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship("Booking", backref="customer", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    registration_number = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer)
    fuel_type = db.Column(db.String(30))
    color = db.Column(db.String(40))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="vehicle", lazy=True)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    specialization = db.Column(db.String(120))
    experience = db.Column(db.Integer, default=0)
    status = db.Column(db.String(30), default="Available")

    bookings = db.relationship("Booking", backref="mechanic", lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    estimated_duration = db.Column(db.String(50))
    status = db.Column(db.String(30), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanic.id"))
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(40), default="Pending")
    problem_description = db.Column(db.Text)
    estimated_cost = db.Column(db.Float, default=0)
    final_cost = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship("BookingService", backref="booking", lazy=True, cascade="all, delete-orphan")
    parts = db.relationship("BookingPart", backref="booking", lazy=True, cascade="all, delete-orphan")
    invoice = db.relationship("Invoice", backref="booking", uselist=False, cascade="all, delete-orphan")
    review = db.relationship("Review", backref="booking", uselist=False, cascade="all, delete-orphan")

class BookingService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    service = db.relationship("Service")

class SparePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    part_number = db.Column(db.String(80))
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    status = db.Column(db.String(30), default="Available")

class BookingPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey("spare_part.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    part = db.relationship("SparePart")

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), unique=True, nullable=False)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    subtotal = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    payment_status = db.Column(db.String(30), default="Unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    discount_percent = db.Column(db.Float, default=0)
    code = db.Column(db.String(50))
    valid_until = db.Column(db.Date)
    status = db.Column(db.String(30), default="Active")
