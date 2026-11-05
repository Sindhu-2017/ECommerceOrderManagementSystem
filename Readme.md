# E-Commerce Order Management System

## Project Overview
The E-Commerce Order Management System is developed using Python, FastAPI and PostgreSQL. It allows customers to register, log in, browse available products, search and filter products, manage their wishlists and place orders. Admin can manage products and monitor customer orders.
The system manages customer details, product information, wishlist items, orders, order items and shipping details through relational database tables.
It also provides JWT-based authentication, role-based authorization, input validation, exception handling, logging and API testing using Pytest.
SQLAlchemy ORM is used for database operations, and Alembic is used for database migrations. PostgreSQL stored procedures and triggers are implemented for selected database operations.

## Main Features

- Customer registration, login, token refresh, logout and profile retrieval.
- Role-based access for customers and administrators.
- Category and product creation, retrieval, update and deletion.
- Product image upload.
- Customer shipping-address management.
- Order creation and order retrieval.
- Wishlist management.
- Razorpay payment creation and payment-status verification.
- Sales summary and product sales reports.
- Request logging, correlation IDs and centralized application exception handling.
- Unit, integration and API tests using Pytest.


## Project Folder Structure

```text
ECommerceOrderManagementSystem/
│
├── alembic/
│   ├── versions/
│   │   ├── 5c58573a046a_creating_tables.py
│   │   ├── b30c390e4fda_payment_table_change.py
│   │   └── b50faff8b76f_creating_all_tables.py
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
| `app/` | Contains the main application source code. |
| `app/main.py` | Initializes the FastAPI application, middleware, exception handlers and API routers. |
| `app/api/routers/` | Contains API route definitions for each module. |
| `app/api/dependencies/` | Provides database sessions, authentication and service dependencies. |
| `app/core/` | Contains application configuration, security utilities, exceptions and logging setup. |
| `app/database/` | Manages database connections and SQLAlchemy model metadata. |
| `app/middleware/` | Contains request logging and observability middleware. |
| `app/models/` | Defines SQLAlchemy database models and relationships. |
| `app/schemas/` | Defines Pydantic request and response schemas for data validation. |
| `app/repositories/interfaces/` | Defines repository contracts for database operations. |
| `app/repositories/implementations/` | Implements database operations using SQLAlchemy. |
| `app/services/` | Contains business logic and application operations. |
| `app/scripts/` | Contains utility scripts, including administrator account creation. |
| `sql/` | Contains PostgreSQL stored procedures and trigger scripts. |
| `alembic/` | Contains database migration configuration and revision files. |
| `tests/unit/` | Contains unit tests for individual services and business logic. |
| `tests/integration/` | Tests interactions between services, repositories and the database. |
| `tests/api/` | Tests API endpoints, responses and access control. |
| `tests/conftest.py` | Defines shared pytest fixtures and test configurations. |
| `uploads/` | Stores uploaded product images. |
| `logs/` | Stores application information and error logs. |
| `pyproject.toml` | Contains Ruff linting and formatting configuration. |
| `requirements.txt` | Lists the Python dependencies required by the project. |
| `alembic.ini` | Contains Alembic migration configuration. |
| `.env.example` | Provides a template for application environment variables. |
| `.gitignore` | Specifies files and folders excluded from Git tracking. |
| `README.md` | Provides project information, setup instructions and usage documentation. |


### Application Architecture
The application follows a layered architecture:

- **Router Layer:** Handles HTTP requests and responses.
- **Schema Layer:** Validates incoming data and structures API responses.
- **Service Layer:** Implements business logic.
- **Repository Layer:** Handles database operations through interfaces and implementations.
- **Model Layer:** Defines database tables and relationships.
- **Database Layer:** Manages database connectivity and SQLAlchemy configuration.


## Database Tables

The application uses PostgreSQL with SQLAlchemy ORM to store and manage data. The database contains the following tables:

| Table Name | Primary Key | Description |
|---|---|---|
| `users` | `user_id` | Stores user login credentials, email, role and account status. |
| `customers` | `customer_id` | Stores customer profile information linked to user accounts. |
| `categories` | `category_id` | Stores product categories and their active status. |
| `products` | `product_id` | Stores product details, price, stock quantity, image path and category information. |
| `shipping` | `shipping_id` | Stores customer shipping addresses and default address information. |
| `orders` | `order_id` | Stores customer orders, order status, total amount and shipping address details. |
| `order_items` | `order_item_id` | Stores products, quantities, unit prices and subtotals for each order. |
| `payments` | `payment_id` | Stores payment details, payment status and Razorpay transaction references. |
| `refresh_tokens` | `refresh_token_id` | Stores hashed refresh tokens, expiration and revocation information. |
| `wishlists` | `wishlist_id` | Stores products added to customer wishlists. |


### Table Relationships

The database uses primary keys and foreign keys to maintain relationships between tables.

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


### Important Database Operations(Stored Procedure and Trigger)

- **Stored Procedure:** `sp_insert_category` is used for inserting product categories.
- **Trigger:** `trg_update_stock` automatically updates product stock when order items are inserted.


## Technology Stack

Programming language-Python 
API framework -FastAPI
Database -PostgreSQL 
ORM - SQLAlchemy (async) 
Database migrations -Alembic 
Data validation - Pydantic
Authentication - JWT 
Payment integration -Razorpay 
Testing -Pytest, pytest-asyncio, HTTPX 
Code quality - Ruff 




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

Create a local `.env` file using `.env.example` as the template. Update the values for your own development environment. Do not commit `.env` or share real passwords, secret keys or payment credentials.

The application configuration expects these settings:
- `PROJECT_NAME`
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `SECRET_KEY`, `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `EMAIL_SENDER`, `EMAIL_PASSWORD` (when email functionality is configured)
- `LOG_LEVEL`
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`

Load the data from .env using the settings defined in `app/core/config.py`.

### 5. Prepare the PostgreSQL database

Create a PostgreSQL database and make sure the database connection values in `.env` point to it.

Apply the database migrations:

```powershell
alembic upgrade head
```

Run the SQL scripts in the `sql/` directory against the configured PostgreSQL database when setting up the stored procedure and trigger:

- `sql/sp_insert_category.sql`
- `sql/trg_update_stock.sql`

These scripts use PostgreSQL-specific SQL.

### 6. Start the application

```powershell
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.




## Database Migration with Alembic

Alembic is used to manage database schema changes and maintain migration history.

### 1. Create a new migration

After modifying SQLAlchemy models, generate a migration file:

```powershell
alembic revision --autogenerate -m "description_of_change"
```

### 2. Apply all migrations

```powershell
alembic upgrade head
```

### 3. Apply a specific migration revision

```powershell
alembic upgrade <revision_id>
```

### 4. Check the current migration revision

```powershell
alembic current
```

### 5. View migration history

```powershell
alembic history
```

### 6. Roll back the latest migration

```powershell
alembic downgrade -1
```

### 7. Roll back to a specific revision

```powershell
alembic downgrade <revision_id>
```


## API Documentation

FastAPI provides interactive API documentation automatically:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Use the authentication endpoints to obtain an access token. For protected endpoints, provide the token through Swagger's **Authorize** control or an HTTP `Authorization: Bearer <access_token>` header.

## API Modules

Authentication ---> Register, login, refresh token, logout and get current profile (`/api/auth`) 
Categories  ---> Create, list, retrieve, update, delete and restore categories (`/api/categories`)
Products ---> Create, list, retrieve, update, delete, restore and upload product images (`/api/products`) 
Customers ---> Administrator customer listing (`/api/admin`) 
Shipping --->Create, list, retrieve, update and delete shipping addresses (`/api/shipping`) 
Wishlists ---> Add, list and remove wishlist products (`/api/wishlists`) 
Orders   ---> Create and retrieve orders (`/orders`) 
Payments --->Create and verify payments (`/payments`) 
Reports   ---> Sales summary and product sales (`/api/reports`) 

Access to some operations depends on the authenticated user's role.


## Running Tests

Run the complete test suite from the project root:

```powershell
python -m pytest -v
```

Run a specific group:

```powershell
python -m pytest tests/unit -v
python -m pytest tests/integration -v
python -m pytest tests/api -v
```



## Development Notes

- Keep API endpoint definitions in `app/api/routers/`.
- Keep business logic in `app/services/`.
- Keep database operations in repository implementations under `app/repositories/implementations/`.
- Define repository contracts under `app/repositories/interfaces/`.
- Keep request and response validation schemas in `app/schemas/`.
- Add new database schema changes through Alembic migrations.
- Keep credentials and environment-specific values outside source control.
- Add tests for new functionality and run the quality checks before pushing changes.

