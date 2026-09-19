# 🚗 AutoCare — Vehicle Service Management Platform

**AutoCare** is a full-stack vehicle service management platform built with **Flask, PostgreSQL/Supabase, SQLAlchemy, and Bootstrap**. It provides a centralized platform for customers and administrators to manage vehicles, services, bookings, mechanics, inventory, invoices, payments, reviews, and offers.

## 🌐 Live Demo

**🔗 Hosted Application:**
https://autocare-noxb.onrender.com/

> The application is deployed on **Render** and uses **Supabase PostgreSQL** for database services.

---

## ✨ Features

### 👤 Customer Management

* Customer registration and login
* Secure authentication
* Vehicle management
* Service booking
* Booking status tracking
* Customer ratings and reviews

### 🛠️ Service Management

* Service catalog
* Service pricing
* Service bookings
* Booking status management
* Mechanic assignment

### 👨‍🔧 Mechanic Management

* Mechanic management
* Service assignment
* Booking tracking

### 📦 Inventory Management

* Spare-parts inventory
* Inventory tracking

### 🧾 Billing & Payments

* Invoice generation
* PDF invoice generation
* Invoice storage using Supabase Storage
* Payment status tracking

### 🎁 Offers

* Service offers
* Offer management
* Customer-facing offers

### 📊 Admin Dashboard

* Centralized administration
* Customer management
* Vehicle management
* Service management
* Booking management
* Mechanic management
* Inventory management
* Invoice and payment tracking

### 🎨 User Interface

* Responsive Bootstrap interface
* Custom CSS styling
* Mobile-friendly design
* Clean and user-friendly layouts

---

## 🧰 Tech Stack

| Category          | Technology           |
| ----------------- | -------------------- |
| Backend           | Flask                |
| ORM               | Flask-SQLAlchemy     |
| Database          | PostgreSQL           |
| Database Platform | Supabase             |
| Authentication    | Flask-Login          |
| Storage           | Supabase Storage     |
| PDF Generation    | ReportLab            |
| Frontend          | HTML, CSS, Bootstrap |
| Deployment        | Render               |
| Database Driver   | Psycopg              |

---

## 📁 Project Structure

```text
AutoCare/
│
├── app/
│   ├── models/
│   │   ├── models.py
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── customer.py
│   │   └── main.py
│   │
│   ├── utils/
│   │   ├── invoice.py
│   │   └── supabase_client.py
│   │
│   ├── seed.py
│   └── __init__.py
│
├── config.py
├── run.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Running Locally

## 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AutoCare
```

## 2. Create a Virtual Environment

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file from the example:

### Windows

```powershell
copy .env.example .env
```

Then configure the required environment variables:

```env
SECRET_KEY=your-secret-key

DATABASE_URL=your-database-url

SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co

SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

SUPABASE_STORAGE_BUCKET=invoices
```

## 5. Run the Application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 🗄️ Supabase PostgreSQL Setup

AutoCare can use **Supabase PostgreSQL** as its production database.

### Steps

1. Create a project in the Supabase Dashboard.
2. Open the project's **Connect** panel.
3. Copy the PostgreSQL connection string.
4. Add it to `.env` as `DATABASE_URL`.

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres
```

For Render or other IPv4-only hosting environments, use the **Supavisor Session Pooler** connection string when the direct database endpoint is not reachable.

When the application starts, Flask-SQLAlchemy creates the application tables through:

```python
db.create_all()
```

> For production applications with evolving schemas, using a migration system such as Alembic or Flask-Migrate is recommended.

---

# ☁️ Supabase Storage

AutoCare uses **Supabase Storage** to store invoice PDFs.

Create a storage bucket named:

```text
invoices
```

Then configure:

```env
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co

SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY

SUPABASE_STORAGE_BUCKET=invoices
```

When an invoice PDF is generated, AutoCare keeps a local copy and uploads a copy to the configured Supabase Storage bucket.

### 🔐 Security

**Never expose the Supabase service-role key to the frontend.**

Do not place it in:

* HTML
* JavaScript
* GitHub
* Client-side environment variables
* Public documentation

The service-role key should remain on the Flask backend.

---

# 🚀 Deployment on Render

AutoCare is deployed using **Render**.

### Build Command

```text
pip install -r requirements.txt
```

### Start Command

```text
gunicorn run:app
```

The `run.py` file creates the Flask application using the application factory:

```python
from app import create_app

app = create_app()
```

Therefore, the Gunicorn entry point is:

```text
run:app
```

### Render Environment Variables

Configure the following environment variables in Render:

```text
SECRET_KEY
DATABASE_URL
SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
SUPABASE_STORAGE_BUCKET
```

For the production database connection, the Supabase pooler connection can be used when required for IPv4 connectivity.

---

# 🔐 Security Considerations

This application uses Flask/SQLAlchemy as the trusted backend and connects directly to PostgreSQL.

The Supabase service-role key is used only on the server for Storage operations.

If Supabase's Data API is exposed directly to the browser in the future:

* Enable Row Level Security (RLS)
* Configure least-privilege policies
* Avoid exposing privileged credentials
* Restrict database and storage access appropriately

---

# 🧪 Demo Credentials

For local/demo environments, the seeded demo accounts are:

### Admin

```text
Email: admin@autocare.com
Password: admin123
```

### Customer

```text
Email: customer@autocare.com
Password: customer123
```

> For any publicly accessible deployment, use secure credentials and do not rely on default/demo passwords.

---

# 📌 Production Checklist

Before using AutoCare with real users, consider implementing:

* [ ] CSRF protection
* [ ] Rate limiting
* [ ] Secure password reset
* [ ] Email verification
* [ ] Real payment gateway integration
* [ ] Email/SMS notifications
* [ ] Stronger booking conflict validation
* [ ] Database migrations with Alembic/Flask-Migrate
* [ ] Appropriate Supabase Storage policies
* [ ] Production-grade logging and monitoring
* [ ] Disable Flask debug mode

---

# 📸 Application

**Live Application:**
https://autocare-noxb.onrender.com/

---

## 👨‍💻 Project

**AutoCare — Vehicle Service Management Platform**

Built using **Flask + PostgreSQL/Supabase + Bootstrap**, with deployment on **Render**.
