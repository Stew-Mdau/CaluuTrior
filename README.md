# CaluuTrior

A web development practice project built with Django, HTML, and CSS.

## Overview

CaluuTrior is an e-commerce application developed for learning and practicing web development fundamentals. The project demonstrates the integration of Django backend with HTML and CSS for frontend development.

**Language Composition:**
- HTML: 66.3%
- Python: 33.7%

## Project Details

- **Created:** January 16, 2026
- **Last Updated:** April 21, 2026
- **Default Branch:** main
- **Visibility:** Private
- **License:** None specified

## Tech Stack

- **Backend:** Django 5.2.8
- **Database:** SQLite3
- **Frontend:** HTML, CSS
- **Email Service:** Gmail SMTP

## Features

- **Product Management:** Product listing and browsing functionality
- **User Authentication:** User registration and login system with redirect to product list
- **Email Integration:** Gmail SMTP integration for email notifications
- **Django Admin:** Built-in admin interface for content management
- **Static Files Handling:** CSS, JavaScript, and image management
- **Media Management:** User-uploaded media storage and handling

## Project Structure

```
CaluuTrior/
├── CaluuTrior/          # Project configuration
│   ├── settings.py      # Django settings and configuration
│   ├── urls.py          # URL routing configuration
│   └── wsgi.py          # WSGI application entry point
├── caluu/               # Main Django application
├── static/              # Static files (CSS, JS, images)
├── media/               # User-uploaded media
├── templates/           # HTML templates
└── db.sqlite3           # SQLite database
```

## Configuration

### Database
- **Engine:** SQLite3
- **Default Location:** `db.sqlite3` in project root

### Installed Apps
- Django core apps (admin, auth, sessions, messages, staticfiles)
- `caluu` - Main application

### Authentication
- **Login Redirect:** Product list page
- **Logout Redirect:** Product list page
- Default password validators enabled

### Email Configuration
- **Provider:** Gmail SMTP
- **Host:** smtp.gmail.com
- **Port:** 587
- **TLS Enabled:** Yes

### Static Files
- **URL:** `/static/`
- **Directories:** Global static folder in project root

## Getting Started

### Prerequisites
- Python 3.x
- Django 5.2.8

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Stew-Mdau/CaluuTrior.git
cd CaluuTrior
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Access the application:
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Learning Objectives

This project is designed to practice and demonstrate:
- Django project setup and configuration
- User authentication and authorization
- Database design with Django ORM
- HTML templating
- CSS styling
- Email integration
- Static and media file management
- Django admin interface

## Development Notes

- **Debug Mode:** Currently enabled (not suitable for production)
- **Allowed Hosts:** Configured for localhost and development use
- **Secret Key:** Development key only (not suitable for production)
- **Media Handling:** Configured for user-uploaded file storage

## Future Improvements

- Move to production-ready settings
- Add comprehensive error handling
- Implement automated testing
- Add API functionality
- Enhance UI/UX with modern CSS frameworks
- Add search and filtering capabilities

## Author

Stew-Mdau

## License

Not specified

---

**Note:** This is a practice project. Do not use production credentials (like email passwords) in public repositories. Use environment variables for sensitive configuration.
