from flask import Blueprint, render_template
from app.models.models import Service, Offer

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    services = Service.query.filter_by(status="Active").all()
    offers = Offer.query.filter_by(status="Active").all()
    return render_template("index.html", services=services, offers=offers)

@main_bp.route("/services")
def services():
    return render_template("services.html", services=Service.query.filter_by(status="Active").all())

@main_bp.route("/offers")
def offers():
    return render_template("offers.html", offers=Offer.query.filter_by(status="Active").all())
