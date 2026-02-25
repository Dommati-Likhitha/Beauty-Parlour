# Beauty Bloom Hub Booking Website

This Django project implements a comprehensive booking system for Beauty Bloom Hub, a high-end beauty salon and wellness centre. The responsive frontend features:

- Detailed service listings with image support
- Customer appointment booking and history
- Admin dashboard for managing services, staff, and bookings
- Elegant branding and contact information

The goal is to provide a seamless user experience for both clients and administrators.

## Features

- Home page with hero banner, services, gallery, contact information
- About page
- Services listing
- Customer signup, login, and booking form
- Admin dashboard for managing bookings
- Styled templates using soft pink/purple theme with CSS flexbox/grid
- SQLite database (default)

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
2. Install Django:
   ```bash
   pip install django
   ```
3. Navigate to project root and run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser for admin access:
   ```bash
   python manage.py createsuperuser
   ```
5. Collect static files (optional during development):
   ```bash
   python manage.py collectstatic
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Access the site at http://127.0.0.1:8000/ and the admin panel at http://127.0.0.1:8000/admin/

## Notes

- Add real images to `salon/static/salon/images` and update references in templates.
- Customize color scheme and fonts in `style.css` as desired.
- For production, update `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` in settings.
