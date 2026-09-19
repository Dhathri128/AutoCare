from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.models import User, Vehicle, Mechanic, Service, Booking, BookingService, SparePart, BookingPart, Invoice, Review, Offer

admin_bp = Blueprint("admin", __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return "Forbidden", 403
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    revenue = db.session.query(db.func.coalesce(db.func.sum(Invoice.total), 0)).filter(Invoice.payment_status == "Paid").scalar()
    return render_template(
        "admin/dashboard.html",
        customers=User.query.filter_by(role="customer").count(),
        vehicles=Vehicle.query.count(),
        bookings=Booking.query.count(),
        pending=Booking.query.filter_by(status="Pending").count(),
        mechanics=Mechanic.query.count(),
        services=Service.query.count(),
        revenue=revenue,
        recent=Booking.query.order_by(Booking.created_at.desc()).limit(8).all()
    )

@admin_bp.route("/customers")
@admin_required
def customers():
    return render_template("admin/customers.html", customers=User.query.filter_by(role="customer").order_by(User.created_at.desc()).all())

@admin_bp.route("/bookings")
@admin_required
def bookings():
    return render_template("admin/bookings.html", bookings=Booking.query.order_by(Booking.created_at.desc()).all(), mechanics=Mechanic.query.filter_by(status="Available").all())

@admin_bp.route("/bookings/<int:booking_id>/update", methods=["POST"])
@admin_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = request.form["status"]
    mechanic_id = request.form.get("mechanic_id")
    if mechanic_id:
        booking.mechanic_id = int(mechanic_id)
    final_cost = request.form.get("final_cost")
    if final_cost:
        booking.final_cost = float(final_cost)
    db.session.commit()
    flash("Booking updated.", "success")
    return redirect(url_for("admin.bookings"))

@admin_bp.route("/mechanics", methods=["GET", "POST"])
@admin_required
def mechanics():
    if request.method == "POST":
        m = Mechanic(
            name=request.form["name"], phone=request.form.get("phone"),
            specialization=request.form.get("specialization"),
            experience=int(request.form.get("experience") or 0)
        )
        db.session.add(m)
        db.session.commit()
        flash("Mechanic added.", "success")
        return redirect(url_for("admin.mechanics"))
    return render_template("admin/mechanics.html", mechanics=Mechanic.query.all())

@admin_bp.route("/services", methods=["GET", "POST"])
@admin_required
def services():
    if request.method == "POST":
        service = Service(
            name=request.form["name"], description=request.form.get("description"),
            price=float(request.form["price"]),
            estimated_duration=request.form.get("estimated_duration")
        )
        db.session.add(service)
        db.session.commit()
        flash("Service added.", "success")
        return redirect(url_for("admin.services"))
    return render_template("admin/services.html", services=Service.query.order_by(Service.name).all())

@admin_bp.route("/parts", methods=["GET", "POST"])
@admin_required
def parts():
    if request.method == "POST":
        part = SparePart(
            name=request.form["name"], part_number=request.form.get("part_number"),
            stock=int(request.form.get("stock") or 0), price=float(request.form.get("price") or 0)
        )
        db.session.add(part)
        db.session.commit()
        flash("Spare part added.", "success")
        return redirect(url_for("admin.parts"))
    return render_template("admin/parts.html", parts=SparePart.query.order_by(SparePart.name).all())

@admin_bp.route("/invoices")
@admin_required
def invoices():
    return render_template("admin/invoices.html", bookings=Booking.query.order_by(Booking.created_at.desc()).all())

@admin_bp.route("/invoices/create/<int:booking_id>", methods=["POST"])
@admin_required
def create_invoice(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.invoice:
        flash("Invoice already exists.", "info")
        return redirect(url_for("admin.invoices"))
    subtotal = booking.final_cost or booking.estimated_cost or 0
    tax = round(subtotal * 0.18, 2)
    total = round(subtotal + tax, 2)
    inv = Invoice(
        booking_id=booking.id,
        invoice_number=f"INV-{booking.id:05d}",
        subtotal=subtotal, tax=tax, total=total,
        payment_status="Unpaid"
    )
    booking.status = "Invoice Generated"
    db.session.add(inv)
    db.session.commit()
    flash("Invoice generated.", "success")
    return redirect(url_for("admin.invoices"))

@admin_bp.route("/invoices/<int:invoice_id>/paid", methods=["POST"])
@admin_required
def mark_paid(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    invoice.payment_status = "Paid"
    invoice.booking.status = "Paid"
    db.session.commit()
    flash("Payment marked as paid.", "success")
    return redirect(url_for("admin.invoices"))

@admin_bp.route("/reviews")
@admin_required
def reviews():
    return render_template("admin/reviews.html", reviews=Review.query.order_by(Review.created_at.desc()).all())

@admin_bp.route("/offers", methods=["GET", "POST"])
@admin_required
def offers():
    if request.method == "POST":
        offer = Offer(
            title=request.form["title"], description=request.form.get("description"),
            discount_percent=float(request.form.get("discount_percent") or 0),
            code=request.form.get("code"),
            valid_until=datetime.strptime(request.form["valid_until"], "%Y-%m-%d").date()
        )
        db.session.add(offer)
        db.session.commit()
        flash("Offer added.", "success")
        return redirect(url_for("admin.offers"))
    return render_template("admin/offers.html", offers=Offer.query.order_by(Offer.valid_until.desc()).all())
