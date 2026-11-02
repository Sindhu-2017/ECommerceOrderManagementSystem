# E-Commerce Order Management System
The E-Commerce Order Management System is developed using Python, FastAPI and PostgreSQL. It allows customers to register, log in, browse available products, search and filter products, manage their wishlists and place orders. Admin can manage products and monitor customer orders.
The system manages customer details, product information, wishlist items, orders, order items and shipping details through relational database tables.
It also provides JWT-based authentication, role-based authorization, input validation, exception handling, logging and API testing using Pytest.
SQLAlchemy ORM is used for database operations, and Alembic is used for database migrations. PostgreSQL stored procedures and triggers are implemented for selected database operations.

## .env and .env example
These files contains Database related data like database name,host,port,username, password and project name.
These data can be loaded in config.py which is located in app/core