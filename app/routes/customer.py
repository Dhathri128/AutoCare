from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app import db
from app.models.models import Vehicle, Service, Booking, BookingService, Invoice, Review, Offer, Mechanic
from app.utils.invoice import create_invoice_pdf

customer_bp = Blueprint("customer", __name__)

def customer_only():
    return current_user.is_authenticated and current_user.role == "customer"

@customer_bp.before_request
@login_required
def guard():
    if not customer_only():
        return "Forbidden", 403

@customer_bp.route("/dashboard")
def dashboard():
    bookings = Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.created_at.desc()).limit(5).all()
    vehicles = Vehicle.query.filter_by(customer_id=current_user.id).all()
    return render_template("customer/dashboard.html", bookings=bookings, vehicles=vehicles)

@customer_bp.route("/vehicles", methods=["GET", "POST"])
def vehicles():
    if request.method == "POST":
        vehicle = Vehicle(
            customer_id=current_user.id,
            registration_number=request.form["registration_number"],
            brand=request.form["brand"],
            model=request.form["model"],
            year=int(request.form["year"]) if request.form.get("year") else None,
            fuel_type=request.form.get("fuel_type"),
            color=request.form.get("color")
        )
        db.session.add(vehicle)
        db.session.commit()
        flash("Vehicle added.", "success")
        return redirect(url_for("customer.vehicles"))
    return render_template("customer/vehicles.html", vehicles=Vehicle.query.filter_by(customer_id=current_user.id).all())

@customer_bp.route("/vehicles/delete/<int:vehicle_id>", methods=["POST"])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.filter_by(id=vehicle_id, customer_id=current_user.id).first_or_404()
    if vehicle.bookings:
        flash("Cannot delete a vehicle with booking history.", "warning")
    else:
        db.session.delete(vehicle)
        db.session.commit()
        flash("Vehicle deleted.", "success")
    return redirect(url_for("customer.vehicles"))

@customer_bp.route("/book-service", methods=["GET", "POST"])
def book_service():
    vehicles = Vehicle.query.filter_by(customer_id=current_user.id).all()
    services = Service.query.filter_by(status="Active").all()
    if request.method == "POST":
        vehicle = Vehicle.query.filter_by(id=int(request.form["vehicle_id"]), customer_id=current_user.id).first_or_404()
        service_ids = request.form.getlist("service_ids")
        if not service_ids:
            flash("Select at least one service.", "warning")
            return redirect(url_for("customer.book_service"))
        booking_date = datetime.strptime(request.form["booking_date"], "%Y-%m-%d").date()
        booking = Booking(
            customer_id=current_user.id,
            vehicle_id=vehicle.id,
            booking_date=booking_date,
            booking_time=request.form["booking_time"],
            status="Pending",
            problem_description=request.form.get("problem_description", "")
        )
        db.session.add(booking)
        db.session.flush()
        total = 0
        for sid in service_ids:
            service = Service.query.get(int(sid))
            if service:
                db.session.add(BookingService(booking_id=booking.id, service_id=service.id, price=service.price))
                total += service.price
        booking.estimated_cost = total
        booking.final_cost = total
        db.session.commit()
        flash(f"Booking #{booking.id} created successfully.", "success")
        return redirect(url_for("customer.booking_detail", booking_id=booking.id))
    return render_template("customer/book_service.html", vehicles=vehicles, services=services)

@customer_bp.route("/bookings")
def bookings():
    return render_template("customer/bookings.html", bookings=Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.created_at.desc()).all())

@customer_bp.route("/bookings/<int:booking_id>")
def booking_detail(booking_id):
    booking = Booking.query.filter_by(id=booking_id, customer_id=current_user.id).first_or_404()
    return render_template("customer/booking_detail.html", booking=booking)

@customer_bp.route("/history")
def history():
    bookings = Booking.query.filter_by(customer_id=current_user.id).filter(Booking.status.in_(["Completed", "Paid"])).order_by(Booking.created_at.desc()).all()
    return render_template("customer/history.html", bookings=bookings)

@customer_bp.route("/invoices")
def invoices():
    bookings = Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template("customer/invoices.html", bookings=bookings)

@customer_bp.route("/invoice/<int:booking_id>/pdf")
def invoice_pdf(booking_id):
    booking = Booking.query.filter_by(id=booking_id, customer_id=current_user.id).first_or_404()
    if not booking.invoice:
        flash("Invoice is not available yet.", "warning")
        return redirect(url_for("customer.booking_detail", booking_id=booking.id))
    path = create_invoice_pdf(booking)
    return send_file(path, as_attachment=True, download_name=f"{booking.invoice.invoice_number}.pdf")

@customer_bp.route("/review/<int:booking_id>", methods=["POST"])
def review(booking_id):
    booking = Booking.query.filter_by(id=booking_id, customer_id=current_user.id).first_or_404()
    if booking.status not in ("Completed", "Paid"):
        flash("Review is available after service completion.", "warning")
        return redirect(url_for("customer.booking_detail", booking_id=booking.id))
    if booking.review:
        flash("You already reviewed this booking.", "info")
        return redirect(url_for("customer.booking_detail", booking_id=booking.id))
    rating = max(1, min(5, int(request.form["rating"])))
    review = Review(booking_id=booking.id, customer_id=current_user.id, rating=rating, comment=request.form.get("comment", ""))
    db.session.add(review)
    db.session.commit()
    flash("Thank you for your review!", "success")
    return redirect(url_for("customer.booking_detail", booking_id=booking.id))
