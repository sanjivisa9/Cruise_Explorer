# Cruise Explorer

A secure cruise booking platform built with Django and React.

## Features

- 🌍 Search Cruises: Search cruises by origin, destination, and month.
- 🛏️ Room Booking: Select and book rooms by type and location, with real-time availability updates.
- 🔄 Flexible Booking Options: Choose deck preferences (forward, middle, backward) and room categories (oceanview, suite, etc.).
- 💳 Payment Integration: Confirm bookings and make payments securely.
- 📊 Admin Panel: Manage bookings, refunds, discounts, and promotional codes.
- 📱 Responsive Design: Optimized for both desktop and mobile experiences.

## Tech Stack

### Frontend
- React.js: For building dynamic and responsive UI components.
- React Router: For navigation between pages.
- Axios: For API communication with the backend.

### Backend
- Django REST Framework: For creating robust APIs to handle business logic.

### Database
- PostgreSQL: To store user information, bookings, and cruise details.

## Setup

1. Create and activate virtual environment:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
cd djangobackend
pip install -r requirements.txt
```

3. Create .env file with required environment variables (see .env.example)

4. Create logs directory:
```bash
mkdir logs
chmod 755 logs  # Linux/Mac only
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Run development server:
```bash
python manage.py runserver
```

## Security Features

- JWT Authentication
- SQL Injection Protection
- XSS Protection
- CSRF Protection
- Rate Limiting
- CORS Configuration
- Request Validation
- Secure Password Storage

## API Endpoints

### Public Endpoints
- `GET /api/cruises/` - List all cruises with filtering
- `POST /api/auth/login/` - User login
- `POST /api/auth/signup/` - User registration

### Protected Endpoints
- `GET /api/rooms/<cruise_id>/<room_type>/<location>/` - Get available rooms
- `POST /api/bookings/` - Create booking
- `DELETE /api/bookings/cancel/` - Cancel booking
- `POST /api/auth/logout/` - User logout

## Environment Variables

Required environment variables in `.env`:
- `DJANGO_SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `CORS_ALLOWED_ORIGINS`
- `LOG_DIR`

## Usage

- Search for available cruises using filters like origin, destination, and departure month.
- Select preferred rooms and deck locations.
- Proceed to booking confirmation and payment.
- Manage bookings via the admin panel.
