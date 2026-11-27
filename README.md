# CaluuTrior

A Django-based e-commerce web application for browsing products, managing a shopping cart, placing orders, reporting payments, and administering products and orders.

## Overview

CaluuTrior is a learning project built with Django, HTML, and CSS. It demonstrates user authentication, Django models and forms, template rendering, cart management, order processing, media uploads, email notifications, and a staff-only order management interface.

**Language composition:**

- HTML: 66.3%
- Python: 33.7%

## Features

### Customers

- Register and log in
- Browse available products
- Add products to a shopping cart
- Increase or reduce cart quantities
- Remove items from the cart
- Place direct orders using **Buy Now**
- Checkout all cart items as one transaction
- Report a payment as paid
- View personal order history
- Cancel eligible pending orders

### Staff

- Add, edit, and delete products
- Manage product names, descriptions, prices, images, and stock
- View customer orders
- Confirm customer payments and completed orders
- Return stock when an order is cancelled

### Other functionality

- Django administration interface
- Product image uploads with media handling
- Gmail SMTP email notifications
- SQLite database for development
- Password validation and Django authentication

## Tech Stack

- **Backend:** Django 5.2.8
- **Database:** SQLite 3
- **Frontend:** HTML and CSS
- **Image handling:** Django `ImageField`
- **Email:** Gmail SMTP

## Project Structure

```text
CaluuTrior/
├── CaluuTrior/             # Django project settings and routing
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── caluu/                  # Main application
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
└── db.sqlite3
```

## Requirements

- Python 3.10 or later
- Django 5.2.8
- Pillow
- An SMTP email account for email notifications

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Stew-Mdau/CaluuTrior.git
cd CaluuTrior
```

### 2. Create and activate a virtual environment

**Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django==5.2.8 pillow
```

> `requirements.txt` is recommended before deploying or sharing the project so all dependencies can be installed consistently.

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

The administrator account can access the staff interface and Django admin panel.

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

- Application: <http://127.0.0.1:8000/>
- Admin panel: <http://127.0.0.1:8000/admin/>

## Main Routes

| Route | Purpose |
|---|---|
| `/` | Product list |
| `/register/` | Customer registration |
| `/login/` | Customer login |
| `/cart/` | Shopping cart |
| `/checkout/` | Create a cart order |
| `/my-orders/` | Customer order history |
| `/seller/orders/` | Staff order management |
| `/product/add/` | Add a product (staff only) |
| `/admin/` | Django admin |

## Email Configuration

The project uses Gmail SMTP. Before running it, configure email settings securely using environment variables rather than storing credentials in `settings.py`.

For example:

```python
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
```

Set values in your shell or environment configuration:

```bash
export EMAIL_HOST_USER="your-email@example.com"
export EMAIL_HOST_PASSWORD="your-app-password"
export DEFAULT_FROM_EMAIL="CaluuTrior Shop <your-email@example.com>"
```

On Windows PowerShell:

```powershell
$env:EMAIL_HOST_USER="your-email@example.com"
$env:EMAIL_HOST_PASSWORD="your-app-password"
$env:DEFAULT_FROM_EMAIL="CaluuTrior Shop <your-email@example.com>"
```

Use a Gmail app password instead of a regular account password.

## Development Configuration

The current settings are intended for local development:

- `DEBUG = True`
- SQLite database
- Media files stored in `media/`
- Static files loaded from the application and project directories

Before deployment, the project should:

- Move `SECRET_KEY`, SMTP credentials, debug mode, and allowed hosts to environment variables
- Remove `*` from `ALLOWED_HOSTS`
- Set `DEBUG = False`
- Use HTTPS and secure cookies
- Use a production database instead of SQLite
- Configure static and media file storage for the deployment platform
- Add automated tests

## Payment Notice

The application currently provides a manual payment workflow: users report a payment and staff confirm the order. It does not currently verify transactions with a payment provider. Staff approval is required before an order is marked completed.

Do not use real customer or payment information during development.

## Testing

Run Django checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

Test coverage should include authentication, cart totals, checkout, stock management, payment status changes, authorization, and staff order management.

## Security Notes

- Never commit passwords, API keys, app passwords, or `SECRET_KEY` values.
- If a credential has already been committed, revoke it and generate a replacement.
- Add `.env`, `db.sqlite3`, `media/`, `venv/`, and Python cache files to `.gitignore`.
- Keep local development credentials separate from production credentials.

## Project Details

- **Repository:** <https://github.com/Stew-Mdau/CaluuTrior>
- **Default branch:** `main`
- **Visibility:** Private
- **License:** Not specified

## Author

Stew-Mdau

## License

No license has been specified. A license should be added before others are permitted to reuse or distribute the project.
