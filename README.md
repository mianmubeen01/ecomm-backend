# Django E-commerce Backend

This is a Django-based backend for an e-commerce application, built for internship evaluation purposes.
It provides RESTful APIs for product management, user authentication, cart, order processing,
contact forms, and password reset with OTP, and integrates Stripe for payments.

## Features

- **Product Management:** CRUD operations for products (admin only for create/update/delete).
- **User Authentication:** Registration, JWT login, and user info endpoints.
- **Cart System:** Add, remove, update, and clear items in a user-specific cart.
- **Order Processing:** Place orders from cart, with address, phone, and payment method.
- **Contact Form:** Submit contact messages.
- **Password Reset:** OTP-based password reset via email.
- **Stripe Integration:** Payment session creation for orders.

## Tech Stack
- Python 3
- Django
- Django REST Framework
- SimpleJWT (for authentication)
- Stripe (for payments)

```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the API:**
   - API root: `http://localhost:8000/api/`
   - Admin: `http://localhost:8000/admin/`

## API Endpoints (Examples)

- `POST   /api/register/`         — Register a new user
- `POST   /api/login/`            — Obtain JWT token
- `GET    /api/products/`         — List products
- `POST   /api/cart/add_item/`    — Add item to cart
- `POST   /api/orders/`           — Place an order
- `POST   /api/contact/`          — Submit contact form
- `POST   /api/forgot-password/`  — Request OTP for password reset
- `POST   /api/verify-otp/`       — Verify OTP
- `POST   /api/reset-password/`   — Reset password
- `POST   /api/stripe/`           — Create Stripe payment session

## Notes
- Make sure to set up your Stripe API keys in `settings.py` for payment integration.
- Media files (product images) are stored in the `media/` directory.
- For full API documentation, see the code in `core/serializers.py` and `core/views.py`.

## License
This project is for educational and Practice purposes.
