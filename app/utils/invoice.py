from pathlib import Path
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.utils.supabase_client import get_supabase

def create_invoice_pdf(booking):
    out_dir = Path("instance/invoices")
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{booking.invoice.invoice_number}.pdf"
    path = out_dir / filename

    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, y, "AUTOCARE")
    y -= 25
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Vehicle Service Center")
    y -= 40

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Invoice: {booking.invoice.invoice_number}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Customer: {booking.customer.name}")
    y -= 15
    c.drawString(50, y, f"Vehicle: {booking.vehicle.brand} {booking.vehicle.model} ({booking.vehicle.registration_number})")
    y -= 15
    c.drawString(50, y, f"Booking Date: {booking.booking_date} {booking.booking_time}")
    y -= 30

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Service")
    c.drawString(400, y, "Amount")
    y -= 18
    c.setFont("Helvetica", 10)

    for item in booking.services:
        c.drawString(50, y, item.service.name)
        c.drawRightString(450, y, f"Rs. {item.price * item.quantity:,.2f}")
        y -= 16

    for item in booking.parts:
        c.drawString(50, y, item.part.name)
        c.drawRightString(450, y, f"Rs. {item.price * item.quantity:,.2f}")
        y -= 16

    y -= 10
    c.line(50, y, 450, y)
    y -= 20
    c.drawString(300, y, "Subtotal:")
    c.drawRightString(450, y, f"Rs. {booking.invoice.subtotal:,.2f}")
    y -= 18
    c.drawString(300, y, "GST (18%):")
    c.drawRightString(450, y, f"Rs. {booking.invoice.tax:,.2f}")
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(300, y, "TOTAL:")
    c.drawRightString(450, y, f"Rs. {booking.invoice.total:,.2f}")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Payment Status: {booking.invoice.payment_status}")
    y -= 40
    c.drawString(50, y, "Thank you for choosing AutoCare!")
    c.save()

    # Upload a copy to Supabase Storage when configured.
    supabase = get_supabase()
    bucket = os.getenv("SUPABASE_STORAGE_BUCKET", "invoices")
    if supabase:
        try:
            with open(path, "rb") as f:
                supabase.storage.from_(bucket).upload(
                    f"{booking.customer_id}/{filename}",
                    f,
                    file_options={"content-type": "application/pdf", "upsert": "true"}
                )
        except Exception:
            # Local PDF remains available even if Storage is not configured yet.
            pass

    return path
