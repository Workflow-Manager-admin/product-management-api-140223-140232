# Product API Backend - Architecture Documentation

## Overview

This backend implements a REST API for managing Product resources using Flask, SQLAlchemy, and Marshmallow, following clean architecture principles. The goal is to separate concerns, ensure maintainability, and provide clear documentation.

---

## Structure

```
product_api_backend/
    app/
        models/
            product.py        # SQLAlchemy Product model (database structure)
        schemas/
            product.py        # Marshmallow schema for serialization, validation
        services/
            product_service.py # Business logic, database handling, decoupled from web
        controllers/
            product_controller.py # Flask views/controllers: API definition
        routes/
            health.py         # Health check endpoint
            product.py        # Blueprint registration for product routes
        database.py           # SQLAlchemy engine/session, DB init
        errors.py             # Application-wide error handlers
        __init__.py           # Flask app creation, API and Blueprint registration
    run.py                    # Entrypoint for app: launches Flask server
    requirements.txt          # Python dependencies
    interfaces/openapi.json   # OpenAPI docs for endpoints
    ARCHITECTURE.md           # (This file) - Documentation
```

---

## Layered/Clean Architecture

- **Models**: Define the Product structure for database with SQLAlchemy (no Flask logic).
- **Schemas**: Marshmallow schemas for input validation and output serialization.
- **Services**: Handle retrieval, update, creation and deletion, isolating business/data logic from API.
- **Controllers**: Handle HTTP requests, calling services, validating with schemas, returning responses.
- **Routes**: Register blueprints for Flask-Smorest; decouples route path assignment.
- **Errors**: Centralizes error handling, ensures uniform error messages.
- **database.py**: Creates and initializes the SQLite engine and session.
- **Initialization**: All DB setup runs at app startup.

---

## Database

- Uses SQLite for simplicity.
- Database file path taken from the `SQLITE_DB` environment variable (default: `sqlite:///products.db`)
- Automatically creates tables on app startup if not present.

---

## API Endpoints

- `GET    /products`        – Get all products
- `POST   /products`        – Create a new product
- `GET    /products/<id>`   – Get product by ID
- `PUT    /products/<id>`   – Update product by ID
- `DELETE /products/<id>`   – Delete product by ID

All payloads are validated and serialized by Marshmallow schemas.

---

## Error Handling

- Validation errors return JSON with code, status, message, and a detailed dictionary of errors.
- 404 Not Found and 400 Bad Request uniformly return JSON.
- Additional error handling can be done by extending `errors.py`.

---

## Adding New Resources

To extend the API:
1. Create new SQLAlchemy model in `models/`.
2. Create Marshmallow schema in `schemas/`.
3. Add service for business/data logic in `services/`.
4. Expose resource controllers in `controllers/`.
5. Register new blueprint (route) in `routes/`.
6. Register blueprint in `__init__.py`.
7. Document endpoint in OpenAPI spec.

---

## Architecture Diagram

```
[Flask App] --> [routes/*.py] --> [controllers/*.py] --> [services/*.py] --> [models/*.py] <--> [database.py]
                                   |                                             ^
                                   v                                             |
                             [schemas/*.py]_____________[marshmallow validation]_/
```
---

## Environment Variables

- **SQLITE_DB**: Path/URL to SQLite database. (e.g., `/tmp/data.sqlite`, `sqlite:///products.db`)
