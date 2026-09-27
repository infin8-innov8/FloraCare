# FloraCare — Django + MySQL Healthcare Coordination Platform

## Overview
FloraCare is a healthcare coordination and resource management platform designed for small clinics. It facilitates patient management, appointment coordination, ambulance resource allocation, and blood bank inventory tracking.

This is a solo hackathon MVP built within a 4-hour implementation budget, optimized for "working and demoable" over "complete and polished."

## Tech Stack

- **Backend**: Python 3.12+, Django 5+, MySQL (via mysqlclient), python-dotenv
- **Database**: MySQL (required), with SQLite fallback for Cloud Run deployment
- **Frontend**: Bootstrap 5 (CDN), Chart.js (CDN), Leaflet.js (CDN) + OpenStreetMap tiles
- **Static Files**: Whitenoise
- **Deployment**: Gunicorn, Docker, Google Cloud Run + Cloud SQL for MySQL
- **Authentication**: Django built-in LoginView/LogoutView, `login_required` via shared mixin

## Key Design Decisions

- **No DRF, Celery, Redis**: Kept simple for hackathon scope
- **Generic CBVs maximized**: ListView, CreateView, DetailView for all CRUD operations
- **Admin-only Updates/Deletes**: All models registered in Django Admin with useful `list_display`, `search_fields`, `list_filter`
- **Optimistic Concurrency Control (OCC)**: Mandatory version field on Appointment model with atomic UPDATE using `F('version') + 1`
- **Server-side Haversine**: Ambulance distance calculation computed server-side in Python, not client-side JS
- **Two charts only**: Pie chart (appointment status) + Bar chart (blood inventory by group), data passed via `json_script`
- **Bootstrap 5 only**: No custom CSS beyond utility classes

## Local Setup

### Prerequisites
- Python 3.12+
- MySQL server running
- `gcloud` CLI (for Cloud SQL connection)

### 1. Clone and Install
```bash
git clone <repository-url>
cd florafit
source .venv/bin/activate  # or: python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env` and configure MySQL credentials:
```
SECRET_KEY=hrn$2#mw67lirgxcql*+qxe!e_0rre#77e0th_)4*#47)+usy8
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL Database
DB_NAME=proto_db
DB_USER=proto_user
DB_PASSWORD='acti8*o'
DB_HOST=localhost
DB_PORT=3306
```

### 3. Database Migrations
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver 0:8000
```
Visit http://127.0.0.1:8000 and login with admin credentials.

### 6. Seed Demo Data (optional)
```bash
python manage.py seed_data
```

## Docker + Cloud Run Deployment

### Dockerfile
```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE ${PORT}

CMD gunicorn proto.wsgi:application --bind 0.0.0.0:${PORT} --workers 2
```

### Cloud SQL for MySQL Setup

1. **Create Cloud SQL instance**:
```bash
gcloud sql instances create floracare-instance \
    --database-version=MYSQL_8_0 \
    --region=us-central1
```

2. **Create database and user**:
```bash
gcloud sql databases create floracare_db --instance=floracare-instance
gcloud sql users create floracare_user --instance=floracare-instance --password=your_password
```

3. **Configure connection**:
```bash
gcloud sql connect floracare-instance --user=floracare_user --database=floracare_db
```

4. **Cloud Run deployment with Cloud SQL**:
```bash
gcloud run deploy floracare-service \
    --image=us-central1-docker.pkg.dev/PROJECT-ID/floracare-repo/floracare:latest \
    --region=us-central1 \
    --port 8080 \
    --add-cloudsql-connection PROJECT:us-central1:floracare-instance
```

5. **Set DATABASE settings in environment**:
   - The Cloud SQL connector automatically sets `DATABASE_URL` or you can use the Unix socket path:
   ```
   DATABASE_URL=mysql+pymysql://floracare_user:your_password/@/floracare_db?unix_socket=/cloudsql/PROJECT:us-central1:floracare-instance
   ```

### Alternative: Unix Socket Path
In `settings.py`, use:
```python
"HOST": "/cloudsql/PROJECT:REGION:INSTANCE",
"PORT": "",
```
with `OPTIONS`: `{"unix_socket": "/cloudsql/PROJECT:REGION:INSTANCE"}`

## Fallback Path (SQLite for Cloud Run)

If Cloud SQL setup consumes too much time before the deadline:

- Local development continues on MySQL as required
- Deployed Cloud Run demo runs on SQLite as a documented exception
- This is a common, defensible hackathon fallback when "the jury can see it working" is the actual requirement
- **Not default**: Only use if Cloud SQL is not working with time remaining

To enable SQLite fallback, set in `.env`:
```
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Then run:
```bash
python manage.py migrate
```

## README.md Screenshots

![Dashboard](screenshots/dashboard.png)
![Patients List](screenshots/patients.png)
![Appointments](screenshots/appointments.png)
![Ambulance](screenshots/ambulance.png)
![Blood Bank](screenshots/bloodbank.png)
![Dashboard Charts](screenshots/dashboard-charts.png)

## Features

### App 1 — Patients
- Register new patient (CreateView)
- List patients with pagination
- Search by name or phone
- Detail view for each patient
- Index on `phone` and `blood_group` for fast lookup

### App 2 — Appointments
- Book new appointments
- List with filters: date, status, doctor_name
- **OCC**: Update status with version comparison
  - Atomic UPDATE: `filter(pk=pk, version=submitted_version).update(status=new_status, version=F('version') + 1)`
  - Error if 0 rows matched: "This appointment was modified by another staff member. Please refresh and try again."
- Upcoming appointments dashboard
- Today's metrics: single aggregated query `values('status').annotate(count=Count('id'))`
- `select_related('patient')` to avoid N+1 queries

### App 3 — Ambulance
- Request ambulance with patient details and pickup coordinates
- Seed ambulance units via `python manage.py seed_data`
- Available units sorted by Haversine distance (server-side)
- Static Leaflet map with ambulance + pickup markers
- Filter request list by status (Requested/Dispatched/Completed)

### App 4 — Blood Bank
- Search inventory by blood_group + city (indexed)
- Request blood with requester details and urgency
- Inventory seeded via `python manage.py seed_data`
- Request list filterable by urgency, blood_group, city

### App 5 — Dashboard
- Total patients count
- Appointment counts by status (single aggregated query)
- Ambulance available/busy counts
- Total blood units available
- Pie chart: Appointment status distribution
- Bar chart: Blood inventory by group
- Chart data via `{{ data|json_script:"id" }}` — no separate JSON API endpoint

### Authentication
- Django LoginView/LogoutView
- `login_required` on every view via shared mixin
- No public registration, no patient self-signup

### Admin
All models registered with useful `list_display`, `search_fields`, `list_filter`:
- Patient: name, age, gender, phone, blood_group, created_at
- Appointment: patient, doctor_name, scheduled_time, status, version
- AmbulanceUnit: unit_name, current_location, latitude, longitude, is_available
- AmbulanceRequest: patient_name, phone, pickup_location, status, requested_at
- BloodInventory: blood_group, location_name, city, units_available, last_updated
- BloodRequest: requester_name, phone, blood_group, city, urgency, created_at

## Requirements

```
Django==5.2.17
django-crispy-forms==2.7
django-widget-tweaks==1.5.1
Pillow==12.3.0
PyMySQL==1.2.3
python-dotenv==1.2.3
whitenoise==6.12.0
Chart.js==4.4.0
leaflet==1.9.4
```

## Development Commands

| Command | Description |
|---------|-------------|
| `python manage.py migrate` | Run database migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py runserver 0:8000` | Start development server |
| `python manage.py seed_data` | Seed demo data for ambulances and blood bank |
| `python manage.py check` | Check system health |

## Deployment Checklist

- [ ] Cloud SQL instance created and reachable
- [ ] Database and user created
- [ ] `requirements.txt` with pinned versions
- [ ] Dockerfile built and pushed to Container Registry
- [ ] Cloud Run service deployed with Cloud SQL connection
- [ ] Whitenoise middleware configured for static file serving
- [ ] Domain/HTTPS configured via Cloud Run
- [ ] README.md updated with deployment steps