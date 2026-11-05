# E-Commerce Order Management System

## Project Overview
The E-Commerce Order Management System is developed using Python, FastAPI and PostgreSQL. It allows customers to register, log in, browse available products, search and filter products, manage their wishlists and place orders. Admin can manage products and monitor customer orders.
The system manages customer details, product information, wishlist items, orders, order items and shipping details through relational database tables.
It also provides JWT-based authentication, role-based authorization, input validation, exception handling, logging and API testing using Pytest.
SQLAlchemy ORM is used for database operations, and Alembic is used for database migrations. PostgreSQL stored procedures and triggers are implemented for selected database operations.

## Main Features

- Customer registration, login, token refresh, logout and profile retrieval.
- Role-based access for customers and administrators.
- Category and product management.
- Product search, filtering and pagination.
- Product image upload.
- Customer shipping-address management.
- Order creation and order retrieval.
- Wishlist management.
- Razorpay payment creation and verification.
- Sales summary and product sales reports.
- Logging and correlation ID tracking.
- Unit, integration and API testing using Pytest.
- PostgreSQL stored procedure and trigger.

## Project Folder Structure

```text
ECommerceOrderManagementSystem/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   │   ├── auth.py
│   │   │   ├── database.py
│   │   │   └── service_depencies.py
│   │   └── routers/
│   │       ├── auth_router.py
│   │       ├── category_router.py
│   │       ├── customer_router.py
│   │       ├── health_router.py
│   │       ├── order_router.py
│   │       ├── payment_router.py
│   │       ├── product_router.py
│   │       ├── report_router.py
│   │       ├── shipping_router.py
│   │       └── wishlist_router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   ├── logging_config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── connection.py
│   │
│   ├── middleware/
│   │   └── observability.py
│   │
│   ├── models/
│   │   ├── category.py
│   │   ├── customer.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   ├── payment.py
│   │   ├── product.py
│   │   ├── refresh_token.py
│   │   ├── shipping.py
│   │   ├── user.py
│   │   └── wishlist.py
│   │
│   ├── repositories/
│   │   ├── interfaces/
│   │   └── implementations/
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── category_schema.py
│   │   ├── customer_schema.py
│   │   ├── order_schema.py
│   │   ├── payment_schema.py
│   │   ├── product_schema.py
│   │   ├── report_schema.py
│   │   ├── shipping_schema.py
│   │   └── wishlist_schema.py
│   │
│   ├── scripts/
│   │   └── create_admin.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── category_service.py
│   │   ├── customer_service.py
│   │   ├── email_service.py
│   │   ├── order_service.py
│   │   ├── payment_service.py
│   │   ├── product_service.py
│   │   ├── report_service.py
│   │   ├── shipping_service.py
│   │   └── wishlist_service.py
│   │
│   └── main.py
│
├── sql/
│   ├── sp_insert_category.sql
│   └── trg_update_stock.sql
│
├── tests/
│   ├── api/
│   ├── integration/
│   ├── unit/
│   └── conftest.py
│
├── uploads/
├── logs/
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Folder and File Descriptions

| Folder / File | Description |
|---|---|
| `app/` | Contains the application source code. |
| `app/main.py` | Starts the FastAPI application and registers middleware, exception handlers and routers. |
| `app/api/routers/` | Contains the API endpoints. |
| `app/api/dependencies/` | Contains database, authentication and service dependencies. |
| `app/core/` | Contains configuration, security, exceptions and logging setup. |
| `app/database/` | Handles database connections and model metadata. |
| `app/middleware/` | Contains request logging and observability middleware. |
| `app/models/` | Defines database tables and relationships. |
| `app/schemas/` | Defines request and response schemas. |
| `app/repositories/interfaces/` | Defines repository interfaces. |
| `app/repositories/implementations/` | Contains database operation implementations. |
| `app/services/` | Contains application business logic. |
| `app/scripts/` | Contains utility scripts such as admin creation. |
| `sql/` | Contains stored procedure and trigger scripts. |
| `alembic/` | Contains database migration files. |
| `tests/unit/` | Contains unit tests. |
| `tests/integration/` | Contains integration tests. |
| `tests/api/` | Contains API endpoint tests. |
| `tests/conftest.py` | Contains shared test fixtures. |
| `uploads/` | Stores uploaded product images. |
| `logs/` | Stores application and error logs. |
| `pyproject.toml` | Contains Ruff configuration. |
| `requirements.txt` | Lists project dependencies. |
| `.env.example` | Provides the environment variable template. |
| `alembic.ini` | Contains Alembic configuration. |
| `README.md` | Contains project documentation. |

### Application Architecture

The application follows a layered architecture.

- **Router Layer:** Handles incoming API requests.
- **Schema Layer:** Validates request data and structures responses.
- **Service Layer:** Handles business logic.
- **Repository Layer:** Handles database operations using interfaces and implementations.
- **Model Layer:** Defines database tables and relationships.
- **Database Layer:** Manages database connections.

## Database Tables

The application uses PostgreSQL with SQLAlchemy ORM.

| Table Name | Primary Key | Description |
|---|---|---|
| `users` | `user_id` | Stores login credentials, email, role and account status. |
| `customers` | `customer_id` | Stores customer profile details. |
| `categories` | `category_id` | Stores product categories. |
| `products` | `product_id` | Stores product details, price, stock and image path. |
| `shipping` | `shipping_id` | Stores customer shipping addresses. |
| `orders` | `order_id` | Stores order details and status. |
| `order_items` | `order_item_id` | Stores products and quantities in each order. |
| `payments` | `payment_id` | Stores payment details and transaction references. |
| `refresh_tokens` | `refresh_token_id` | Stores refresh token information. |
| `wishlists` | `wishlist_id` | Stores products added to customer wishlists. |

### Table Relationships

| Parent Table | Child Table | Relationship |
|---|---|---|
| `users` | `customers` | One-to-one |
| `users` | `refresh_tokens` | One-to-many |
| `customers` | `shipping` | One-to-many |
| `customers` | `orders` | One-to-many |
| `customers` | `wishlists` | One-to-many |
| `categories` | `products` | One-to-many |
| `products` | `order_items` | One-to-many |
| `products` | `wishlists` | One-to-many |
| `orders` | `order_items` | One-to-many |

### Stored Procedure and Trigger

- **Stored Procedure:** `sp_insert_category` is used to insert product categories.
- **Trigger:** `trg_update_stock` updates product stock when order items are inserted.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | API development |
| PostgreSQL | Database |
| SQLAlchemy | ORM and database operations |
| Alembic | Database migrations |
| Pydantic | Data validation |
| JWT | Authentication |
| Razorpay | Payment integration |
| Pytest | Testing |
| HTTPX | API testing |
| Ruff | Code formatting and linting |

## Prerequisites

Install the following before running the application:

- Python 3.11 or a compatible supported version.
- PostgreSQL.
- Git.

## Setup and Installation

### 1. Clone the repository

```powershell
git clone <repository-url>
cd ECommerceOrderManagementSystem
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a template.

Update the values according to your local environment.

The application uses the following settings:

- `PROJECT_NAME`
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SECRET_KEY`
- `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `EMAIL_SENDER`
- `EMAIL_PASSWORD`
- `LOG_LEVEL`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`


### 5. Prepare the PostgreSQL database

Create a PostgreSQL database and update the database details in `.env`.

Run the migrations:

```powershell
alembic upgrade head
```

Run the SQL scripts in the `sql/` folder to create the stored procedure and trigger:

- `sql/sp_insert_category.sql`
- `sql/trg_update_stock.sql`

### 6. Start the application

```powershell
uvicorn app.main:app --reload
```

The application will run at:

`http://127.0.0.1:8000`

## Database Migration with Alembic

Alembic is used to manage database changes.

### Create a new migration

After changing the SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "description_of_change"
```

### Apply all migrations

```powershell
alembic upgrade head
```

### Apply a specific migration

```powershell
alembic upgrade <revision_id>
```

### Check the current migration

```powershell
alembic current
```

### View migration history

```powershell
alembic history
```

### Roll back the latest migration

```powershell
alembic downgrade -1
```

### Roll back to a specific revision

```powershell
alembic downgrade <revision_id>
```

## API Documentation

FastAPI provides Swagger UI for testing the API endpoints.

Swagger UI:

`http://127.0.0.1:8000/docs`

## Authorization

Protected endpoints require a valid access token.

1. Login using `/api/auth/login`.
2. Copy the returned `access_token`.
3. Click **Authorize** in Swagger UI.
4. Enter the access token.
5. Click Authorize.

### User Roles

- **Admin:** Can manage categories, products, customers and reports.
- **Customer:** Can manage shipping addresses, wishlists, orders and payments.
- **Authenticated users:** Can access their own profile.

## 1. Authentication APIs

Base URL: `/api/auth`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Registers a new customer. |
| POST | `/login` | Logs in and generates tokens. |
| POST | `/refresh` | Generates new tokens using a refresh token. |
| POST | `/logout` | Revokes the refresh token. |
| GET | `/me` | Gets the logged-in user's profile. |

### Register

`POST /api/auth/register`

Sample input:

```json
{
  "username": "john123",
  "email": "john@gmail.com",
  "password": "John@123",
  "first_name": "John",
  "last_name": "David",
  "phone": "9876543210",
  "date_of_birth": "2000-05-15"
}
```

### Login

`POST /api/auth/login`

Sample form data:

```text
username: john123
password: John@123
```

Returns access and refresh tokens after successful login.

### Refresh Token

`POST /api/auth/refresh`

Sample input:

```json
{
  "refresh_token": "your_refresh_token"
}
```

### Logout

`POST /api/auth/logout`

Sample input:

```json
{
  "refresh_token": "your_refresh_token"
}
```

### Get My Profile

`GET /api/auth/me`

Returns the logged-in user's details.

## 2. Category APIs

Base URL: `/api/categories`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Creates a category. |
| GET | `/` | Gets all categories. |
| GET | `/{category_id}` | Gets a category by ID. |
| PATCH | `/{category_id}` | Updates a category. |
| DELETE | `/{category_id}` | Deletes a category. |
| GET | `/admin/deleted` | Gets deleted categories. |
| PATCH | `/admin/restore/{category_id}` | Restores a deleted category. |

### Create Category

`POST /api/categories/`

```json
{
  "category_name": "Electronics",
  "description": "Electronic products"
}
```

### Update Category

`PATCH /api/categories/1`

```json
{
  "category_name": "Mobile Phones",
  "description": "Smartphones and accessories"
}
```

Only admin users can manage categories.

## 3. Product APIs

Base URL: `/api/products`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Creates a product. |
| GET | `/` | Gets products with search and filters. |
| GET | `/{product_id}` | Gets a product by ID. |
| PATCH | `/{product_id}` | Updates a product. |
| DELETE | `/{product_id}` | Deletes a product. |
| GET | `/admin/deleted` | Gets deleted products. |
| PATCH | `/admin/restore/{product_id}` | Restores a deleted product. |
| POST | `/{product_id}/image` | Uploads a product image. |

### Create Product

`POST /api/products/`

```json
{
  "category_id": 1,
  "product_name": "Wireless Mouse",
  "description": "Bluetooth wireless mouse",
  "price": 599.00,
  "stock_quantity": 50
}
```

### Get Products

`GET /api/products/`

Optional query parameters:

```text
search=mouse
category_id=1
min_price=100
max_price=1000
skip=0
limit=10
```

### Update Product

`PATCH /api/products/1`

```json
{
  "product_name": "Wireless Mouse",
  "price": 699.00,
  "stock_quantity": 40
}
```

### Upload Product Image

`POST /api/products/1/image`

Select the image file using Swagger's file upload option.

Only admin users can manage products.

## 4. Customer APIs

Base URL: `/api/admin`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/customers` | Gets all registered customers. |

Only admin users can access the customer list.

## 5. Shipping APIs

Base URL: `/api/shipping`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Adds a shipping address. |
| GET | `/` | Gets all saved addresses. |
| GET | `/{shipping_id}` | Gets an address by ID. |
| PATCH | `/{shipping_id}` | Updates an address. |
| DELETE | `/{shipping_id}` | Deletes an address. |

### Create Shipping Address

`POST /api/shipping/`

```json
{
  "recipient_name": "John David",
  "phone": "9876543210",
  "address_line": "12 Main Road",
  "city": "Chennai",
  "state": "Tamil Nadu",
  "pincode": "600001",
  "is_default": true
}
```

### Update Shipping Address

`PATCH /api/shipping/1`

```json
{
  "phone": "9876501234",
  "city": "Coimbatore"
}
```

Customers can save multiple shipping addresses and update their saved addresses.

## 6. Wishlist APIs

Base URL: `/api/wishlists`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/{product_id}` | Adds a product to the wishlist. |
| GET | `/` | Gets wishlist products. |
| DELETE | `/{product_id}` | Removes a product from the wishlist. |

Example:

`POST /api/wishlists/1`

Adds product ID 1 to the logged-in customer's wishlist.

## 7. Order APIs

Base URL: `/orders`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/` | Creates a new order. |
| GET | `/{order_id}` | Gets an order by ID. |
| GET | `/` | Gets the logged-in customer's orders. |
| GET | `/admin/all` | Gets all customers' orders. |

### Create Order

`POST /orders/`

```json
{
  "shipping_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 2,
      "quantity": 1
    }
  ]
}
```

The system calculates the order total using the selected products and quantities.

## 8. Payment APIs

Base URL: `/payments`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/create/{order_id}` | Creates a Razorpay payment link. |
| POST | `/verify/{payment_id}` | Checks the payment status. |

### Create Payment

`POST /payments/create/1`

Creates a Razorpay payment link for the selected order. Open the returned payment URL to complete the payment.

### Verify Payment

`POST /payments/verify/1`

Checks the payment status with Razorpay. If payment is successful, the payment and order statuses are updated.

## 9. Report APIs

Base URL: `/api/reports`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/sales-summary` | Gets overall sales information. |
| GET | `/product-sales` | Gets product-wise sales information. |

- **Sales Summary:** Shows total orders, paid orders, pending orders and total revenue.
- **Product Sales:** Shows the quantity sold and total sales for each product.

These reports are available to admin users.

## 10. Health Check API

Base URL: `/api/health`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks application and database health. |

Sample response:

```json
{
  "status": "healthy",
  "database": "connected"
}
```

## 11. Home API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the API is running. |

Sample response:

```json
{
  "message": "E-Commerce Order Management System API is running"
}
```

## Running Tests

Run all tests from the project root:

```powershell
python -m pytest -v
```

Run specific tests:

```powershell
python -m pytest tests/unit -v
python -m pytest tests/integration -v
python -m pytest tests/api -v
```


