from datetime import date
from app import db
from app.models.models import User, Service, Mechanic, SparePart, Offer, Vehicle

def seed_database():
    if User.query.first():
        return

    admin = User(name="AutoCare Admin", email="admin@autocare.com", phone="9999999999", role="admin")
    admin.set_password("admin123")

    customer = User(name="Demo Customer", email="customer@autocare.com", phone="8888888888", role="customer")
    customer.set_password("customer123")

    db.session.add_all([admin, customer])
    db.session.flush()

    vehicle = Vehicle(
        customer_id=customer.id, registration_number="TS09AB1234",
        brand="Honda", model="City", year=2022, fuel_type="Petrol", color="White"
    )
    db.session.add(vehicle)

    services = [
        Service(name="General Service", description="Complete periodic maintenance and inspection.", price=2500, estimated_duration="3 hours"),
        Service(name="Engine Oil Change", description="Engine oil and basic filter inspection.", price=1500, estimated_duration="1 hour"),
        Service(name="AC Service", description="AC performance check, cleaning and gas inspection.", price=1200, estimated_duration="2 hours"),
        Service(name="Brake Service", description="Brake inspection and maintenance.", price=1800, estimated_duration="2 hours"),
        Service(name="Wheel Alignment", description="Four-wheel alignment and balancing check.", price=900, estimated_duration="1 hour"),
        Service(name="Full Car Wash", description="Exterior wash and interior cleaning.", price=700, estimated_duration="1.5 hours"),
    ]
    db.session.add_all(services)

    mechanics = [
        Mechanic(name="Arun Kumar", phone="9000000001", specialization="Engine & General Service", experience=6),
        Mechanic(name="Vikram Singh", phone="9000000002", specialization="AC & Electrical", experience=5),
        Mechanic(name="Ravi Teja", phone="9000000003", specialization="Brakes & Suspension", experience=7),
    ]
    db.session.add_all(mechanics)

    parts = [
        SparePart(name="Engine Oil", part_number="EO-5W30", stock=40, price=850),
        SparePart(name="Oil Filter", part_number="OF-001", stock=25, price=450),
        SparePart(name="Air Filter", part_number="AF-001", stock=20, price=700),
        SparePart(name="Brake Pad Set", part_number="BP-001", stock=12, price=2500),
        SparePart(name="Car Battery", part_number="BAT-001", stock=8, price=6500),
    ]
    db.session.add_all(parts)

    offers = [
        Offer(title="First Service Offer", description="Get 15% off your first service booking.", discount_percent=15, code="WELCOME15", valid_until=date(2026, 12, 31)),
        Offer(title="Full Service Deal", description="Save 20% on selected full-service packages.", discount_percent=20, code="FULL20", valid_until=date(2026, 11, 30)),
    ]
    db.session.add_all(offers)

    db.session.commit()
