# AutoCare — Vehicle Service Management Platform

A polished Flask + PostgreSQL/Supabase vehicle service management application.

## Included
- Customer registration/login
- Admin dashboard
- Vehicle management
- Service catalog and pricing
- Service booking
- Booking status tracking
- Mechanic management and assignment
- Spare-parts inventory
- Invoice generation + PDF
- Payment status
- Customer ratings/reviews
- Offers
- Supabase PostgreSQL support
- Supabase Storage support for invoice PDFs
- Responsive Bootstrap UI with custom CSS

## 1. Run locally with SQLite
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python run.py
```
Open http://127.0.0.1:5000

Demo admin:
- admin@autocare.com / admin123

Demo customer:
- customer@autocare.com / customer123

## 2. Set up Supabase PostgreSQL
1. Create a project in the Supabase Dashboard.
2. Open the project's **Connect** panel.
3. Copy the PostgreSQL connection string.
4. Put it in `.env` as DATABASE_URL.

Example:
```text
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
```

For Render or another IPv4-only host, use the **Supavisor Session Pooler** connection string from the Connect panel if the direct connection is not reachable.

Then delete the local `autocare.db` if you want a completely fresh database and run:
```powershell
python run.py
```
The Flask application calls `db.create_all()` and creates the application tables in the Supabase PostgreSQL database.

## 3. Configure Supabase Storage
Create a Storage bucket named:
```text
invoices
```

Add these values to `.env`:
```text
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
SUPABASE_STORAGE_BUCKET=invoices
```

**Important:** keep `SUPABASE_SERVICE_ROLE_KEY` only on the Flask server. Never put it in HTML, JavaScript, GitHub, or client-side environment variables.

When an invoice PDF is generated, AutoCare keeps a local copy and uploads a copy to the `invoices` bucket when Storage credentials are configured.

## 4. Supabase security
This architecture uses Flask/SQLAlchemy as the trusted backend and connects directly to PostgreSQL. The Supabase service-role key is used only server-side for Storage.

If you later expose Supabase's Data API directly to the browser, configure Row Level Security (RLS) and least-privilege policies before doing so.

## 5. Render deployment
Build command:
```text
pip install -r requirements.txt
```
Start command:
```text
gunicorn run:app
```

Set the Render environment variables:
- SECRET_KEY
- DATABASE_URL
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- SUPABASE_STORAGE_BUCKET

For Render, prefer the Supabase pooler connection if the direct database endpoint causes an IPv6/IPv4 connectivity problem.

## Production checklist
Before real users:
- Add CSRF protection
- Add rate limiting
- Add secure password reset/email verification
- Add real payment gateway
- Add email/SMS notifications
- Add stronger booking conflict validation
- Add database migrations (Alembic/Flask-Migrate)
- Configure Supabase Storage RLS/policies if using client-side Storage access
- Disable Flask debug mode
