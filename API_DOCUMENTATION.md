# E-Commerce Django REST API Documentation

This document outlines the project structure of the E-commerce backend and provides a step-by-step guide on how to test the API endpoints using Postman.

## 📁 Project Structure

The project follows a modular Django application architecture. The main project folder is `ecommerce`, and the logical components are broken down into individual apps.

```text
backend/
│
├── ecommerce/           # Main Django project configuration folder
│   ├── settings.py      # App configs, JWT, CORS, Database settings
│   ├── urls.py          # Root URL router
│   └── wsgi.py / asgi.py
│
├── users/               # Custom Authentication & User Management
│   ├── models.py        # Custom User model (Email-based, roles: admin/customer)
│   ├── views.py         # Register and Profile Views
│   └── serializers.py   # JWT token claims and User validation
│
├── products/            # Product Catalog Management
│   ├── models.py        # Category and Product models
│   ├── views.py         # ViewSets for searching, filtering, and ordering
│   └── permissions.py   # IsAdminOrReadOnly custom permission
│
├── cart/                # Shopping Cart System
│   ├── models.py        # Cart (1:1 with User) and CartItem (M:1 with Product)
│   ├── views.py         # Add/Remove items, dynamic total calculation
│   └── serializers.py   # Nested serializers for cart structure
│
├── orders/              # Order Management (Pending implementation)
├── payments/            # Payment Processing (Pending implementation)
├── reviews/             # Product Ratings (Pending implementation)
│
├── manage.py            # Django CLI
├── create_admin.py      # Helper script to create an admin user
└── .env                 # Environment variables (Database, Secrets)
```

---

## 🧪 Postman Testing Guide

Ensure the development server is running before testing:
`python manage.py runserver`

### 1. Authentication

**Register a New Customer User**
*   **Method:** `POST`
*   **URL:** `http://127.0.0.1:8000/api/auth/register/`
*   **Body (raw JSON):**
    ```json
    {
        "email": "customer@example.com",
        "password": "StrongPassword123!",
        "password_confirm": "StrongPassword123!",
        "first_name": "Test",
        "last_name": "Customer"
    }
    ```

**Login to get JWT Tokens**
*   **Method:** `POST`
*   **URL:** `http://127.0.0.1:8000/api/auth/login/`
*   **Body (raw JSON):**
    ```json
    {
        "email": "admin@example.com", 
        "password": "AdminPassword123!" 
    }
    ```
    *(Note: Use the admin credentials above to test Product creation, or customer credentials for Cart testing).*
*   **Important Action:** Copy the `access` string from the JSON response.

**How to Authenticate in Postman:**
For all subsequent requests, you must provide the token:
1. Go to the **Authorization** tab in Postman.
2. Select **Bearer Token** as the Type.
3. Paste the `access` token you copied.

---

### 2. Products & Categories

**Create a Category (Admin Token Required)**
*   **Method:** `POST`
*   **URL:** `http://127.0.0.1:8000/api/categories/`
*   **Body (raw JSON):**
    ```json
    {
        "name": "Electronics",
        "description": "Tech gadgets and devices"
    }
    ```

**Create a Product (Admin Token Required)**
*   **Method:** `POST`
*   **URL:** `http://127.0.0.1:8000/api/products/`
*   **Body (raw JSON):**
    ```json
    {
        "name": "Macbook Pro M3",
        "description": "The latest Apple Silicon laptop.",
        "price": "1999.99",
        "stock_quantity": 10,
        "category": 1
    }
    ```

**Fetch and Filter Products (Publicly accessible)**
*   **Method:** `GET`
*   **URL:** `http://127.0.0.1:8000/api/products/`
*   **Search Example:** `http://127.0.0.1:8000/api/products/?search=Macbook`
*   **Price Filter Example:** `http://127.0.0.1:8000/api/products/?price__lte=2000`
*   **Order By Price:** `http://127.0.0.1:8000/api/products/?ordering=price`

---

### 3. Shopping Cart

*(Switch back to your Customer Token in the Authorization tab to test as a normal user)*

**Add Item to Cart**
*   **Method:** `POST`
*   **URL:** `http://127.0.0.1:8000/api/cart/items/`
*   **Body (raw JSON):**
    ```json
    {
        "product": 1,
        "quantity": 2
    }
    ```
    *(If you try to add a quantity > 10, the API will reject it due to the stock validation).*

**View your Cart & Totals**
*   **Method:** `GET`
*   **URL:** `http://127.0.0.1:8000/api/cart/`
*   **Response:** You will see the cart items nested with dynamic `total_price` per item and a `total_amount` for the whole cart.

**Clear the Cart**
*   **Method:** `DELETE`
*   **URL:** `http://127.0.0.1:8000/api/cart/clear/`

---

### 4. Interactive API Documentation (Swagger)

You can also view and test the API directly in your browser without Postman!
Because we integrated `drf-spectacular`, an auto-generated Swagger UI is available at:
👉 **[http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)**
