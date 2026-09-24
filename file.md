# E-Commerce REST API Documentation

This document serves as the complete guide to the API structure, endpoints, and how to test the flow end-to-end using Postman.

---

## 🏗️ Project Architecture & Requirements Checklist

This project was built to satisfy all requirements for learning Django REST Framework:
1. JWT Auth (Login, Register, Refresh, Logout).
2. **User Management:** Profile views, Update, Change Password.
3. **Database:** 9 interconnected Django ORM models.
4. **REST API:** GET, POST, PUT/PATCH, DELETE implemented appropriately.
5. **Serializers:** Nested relationships (Cart/Order items), explicit Validation.
6. **API Views:** Demonstrates Function Based Views (Logout), APIView (Payments), Generic Views (Reviews/Password), Mixins (Orders), and ViewSets (Products).
7. **Validation:** Unique emails, Rating boundaries (1-5), Stock deduction, Amount validation.
8. **Permissions:** Custom `IsAdminOrReadOnly` and Strict object-level ownership checks.
9. **Search & Filtering:** Price filtering and text searching on Products.
10. **Pagination:** Global `PageNumberPagination` (10 items per page).
11. **API Documentation:** Swagger/OpenAPI available at `/api/docs/`.
12. **Testing:** Automated tests for auth, products, carts, and order creation.

---

## 🚀 Postman End-to-End Testing Guide

Ensure the server is running: `python manage.py runserver`
Base URL for all requests: `http://127.0.0.1:8000/api`

### 1. User Authentication & Management

**Register User**
- **Method:** `POST` `/auth/register/`
- **Body:**
  ```json
  {
      "email": "customer@example.com",
      "password": "StrongPassword123",
      "password_confirm": "StrongPassword123"
  }
  ```

**Login & Get JWT Token**
- **Method:** `POST` `/auth/login/`
- **Body:**
  ```json
  {
      "email": "customer@example.com",
      "password": "StrongPassword123"
  }
  ```
> **IMPORTANT:** Copy the `access` token. In Postman, go to **Authorization** -> **Bearer Token** and paste it for ALL following requests.

**Change Password**
- **Method:** `PUT` `/auth/profile/password/`
- **Body:**
  ```json
  {
      "old_password": "StrongPassword123",
      "new_password": "NewStrongPassword123"
  }
  ```

**Logout (Invalidates Token)**
- **Method:** `POST` `/auth/logout/`
- **Body:**
  ```json
  {
      "refresh": "PASTE_YOUR_REFRESH_TOKEN_HERE"
  }
  ```

---

### 2. Catalog (Products & Categories)

> Note: To CREATE products, you must login with an admin account token (e.g., `admin@example.com`).

**Create Product (Admin)**
- **Method:** `POST` `/products/`
- **Body:**
  ```json
  {
      "name": "Wireless Mouse",
      "description": "Ergonomic mouse",
      "price": "29.99",
      "stock_quantity": 50,
      "category": 1
  }
  ```

**List & Search Products (Public)**
- **Method:** `GET` `/products/`
- **Search Query:** `GET` `/products/?search=mouse`
- **Filter Query:** `GET` `/products/?price__lte=50`
- **Pagination:** `GET` `/products/?page=2`

---

### 3. Shopping Flow (Cart ➡️ Order ➡️ Payment)

**Step 1: Add to Cart**
- **Method:** `POST` `/cart/items/`
- **Body:**
  ```json
  {
      "product": 1,
      "quantity": 2
  }
  ```

**Step 2: View Cart Totals**
- **Method:** `GET` `/cart/`
- *Observe the nested items and dynamically calculated `total_amount`.*

**Step 3: Checkout (Create Order)**
- **Method:** `POST` `/orders/`
- **Body:**
  ```json
  {
      "shipping_address": "123 Postman St, API City",
      "phone_number": "+1234567890"
  }
  ```
- *Note: This triggers a database transaction. It deducts the product stock and clears your cart. It returns an `order_number` and `order_id`.*

**Step 4: Pay for Order**
- **Method:** `POST` `/payments/process/`
- **Body:**
  ```json
  {
      "order_id": 1,
      "payment_method": "credit_card"
  }
  ```
- *The order status will update to `processing` and payment status to `paid`.*

---

### 4. Product Reviews

**Leave a Review**
- **Method:** `POST` `/products/1/reviews/`
- **Body:**
  ```json
  {
      "rating": 5,
      "comment": "Excellent product, highly recommended!"
  }
  ```
*(Validation ensures the rating is between 1 and 5, and users can only review a product once).*
