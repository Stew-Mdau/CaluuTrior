# CaluuTrior

A Django-based e-commerce web application for selling non-programmable scientific calculators.

## Overview

CaluuTrior is an online store for non-programmable scientific calculators. Customers can browse calculator products, create an account, manage a shopping cart, place orders, and track their purchases. Staff users can manage products and customer orders.

## Features

### Customers

- Register and log in
- Browse available calculator products
- View product names, descriptions, prices, images, and stock
- Add products to a shopping cart
- Increase or reduce cart quantities
- Remove items from the cart
- Place direct orders using **Buy Now**
- Checkout all cart items as one transaction
- Report payments
- View personal order history
- Cancel eligible pending orders

### Staff

- Add, edit, and delete calculator products
- Manage product descriptions, prices, images, and stock
- View customer orders
- Confirm reported payments
- Complete or cancel orders
- Return stock when an order is cancelled

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
├── caluu/                  # Main store application
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
- An SMTP email account for notifications

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

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

The administrator account can access the Django admin and staff order interface.

### 6. Run the development server

```bash
python manage.py runserver
```

Open:

- Store: <http://127.0.0.1:8000/>
- Admin panel: <http://127.0.0.1:8000/admin/>

## Main Routes

| Route | Purpose |
|---|---|
| `/` | Product catalogue |
| `/register/` | Customer registration |
| `/login/` | Customer login |
| `/cart/` | Shopping cart |
| `/checkout/` | Create a cart order |
| `/my-orders/` | Customer order history |
| `/seller/orders/` | Staff order management |
| `/product/add/` | Add a product (staff only) |
| `/admin/` | Django administration |

## Email Configuration


Use a Gmail app password rather than a regular account password.

## Payment Notice

The application currently uses a manual payment workflow: customers report a payment and staff members approve or complete the order. It does not verify payments through an external payment provider.

## Development Configuration


## Testing

Run Django checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

Test coverage should include authentication, product catalogues, cart totals, checkout, stock management, order status changes, and seller authorization.


## Author

Stew-Mdau
