# Product API Backend - Architecture Documentation

## Overview

The Product API Backend is a modular, maintainable REST API, built using Flask, SQLAlchemy, Marshmallow, and Flask-Smorest. It is designed for managing Product resources with complete CRUD support. The codebase adheres to clean architecture principles, decoupling concerns across well-defined layers: models, schemas, services, controllers, and routes.

SQLite is used as the persistent data store, and all database operations are abstracted via SQLAlchemy ORM. The project emphasizes clear separation of concerns, input validation, robust error handling, and self-documenting code.

---

## Project Structure

```
product_api_backend/
    app/
        models/
            product.py          # SQLAlchemy Product model (database structure)
        schemas/
            product.py          # Marshmallow schema for validation/serialization
        services/
            product_service.py  # Implements business logic and manages DB operations
        controllers/
            product_controller.py # Flask-Smorest controllers for API endpoints
        routes/
            health.py           # / (root) health check endpoint
            __init__.py         # Blueprint package initializer
        database.py             # SQLAlchemy DB session/engine, DB initialization
        errors.py               # Global error handlers for Flask app
        __init__.py             # App factory: creates Flask app, registers blueprints, initializes DB
    run.py                      # Entrypoint: launches Flask app instance
    requirements.txt            # Python dependencies
    interfaces/openapi.json     # OpenAPI documentation for endpoints
    ARCHITECTURE.md             # This file – architecture documentation
```

---

## Architectural Layers and Their Responsibilities

### 1. **Models (`models/`)**
Defines the database tables via SQLAlchemy ORM. `product.py` implements the `Product` model with attributes `id`, `name`, `description`, `price`, and `quantity`. No Flask-specific code exists in this layer—it is pure data modeling.

### 2. **Schemas (`schemas/`)**
Encapsulate input validation, type enforcement, and (de-)serialization using Marshmallow. `ProductSchema` ensures data correctness for all exposed endpoints.

### 3. **Services (`services/`)**
Implements business logic and database access, isolated from HTTP request/response details. The `ProductService` class provides methods for all CRUD actions—retrieving, creating, updating, and deleting products—and manages session usage for DB access.

### 4. **Controllers (`controllers/`)**
Defines Flask-Smorest MethodView controllers that:
- Receive incoming HTTP requests,
- Validate/deserialize input using schemas,
- Call service layer methods,
- Serialize results for API responses,
- Handle error cases and return appropriate status codes.

Blueprints group routes for modular registration. Each controller focuses on one resource type (here, product).

### 5. **Routes (`routes/`)**
Contains blueprint modules to wire controllers/endpoints onto the Flask app, encapsulating URL and resource associations (e.g., registering `/products` or `/` for health).

### 6. **Database (`database.py`)**
Centralizes the database engine configuration, connection, and table initialization logic. Reads the SQLite path/URL from the `SQLITE_DB` environment variable. Calls `Base.metadata.create_all()` on app startup to ensure tables are present.

### 7. **Errors (`errors.py`)**
Registers custom error handlers with Flask. Uniform JSON error responses are returned for validation, 404, 400, and 500 errors.

### 8. **Initialization and Entrypoint**
- `app/__init__.py` initializes Flask, registers CORS, blueprints, error handlers, and triggers DB setup.
- `run.py` is the entry launcher, running Flask's development server.

---

## Data Flow

1. **Incoming HTTP Request**  
   → Routed to the appropriate controller by Flask-Smorest blueprint (`routes/product.py`).
2. **Controller Method (e.g., GET `/products/<id>`)**  
   → Validates and deserializes data using Marshmallow schema.
3. **Service Layer**  
   → Controller delegates to appropriate service method, which performs ORM operations with a dedicated session.
4. **Database Layer (SQLAlchemy ORM, SQLite)**  
   → All queries/commands take place using SQLAlchemy, and data are committed/rolled back as needed.
5. **Response Serialization**  
   → Results are serialized with schemas before being returned by the controller.
6. **Outgoing HTTP Response**  
   → JSON payload with result data and appropriate HTTP status, or uniform error if applicable.

---

## REST API Structure & Endpoints

All endpoints are mounted below `/products` except health check:

| HTTP Verb | Path                | Description                | Request Body         | Response            |
|-----------|---------------------|----------------------------|----------------------|---------------------|
| GET       | `/products`         | Retrieve all products      | —                    | Array of products   |
| POST      | `/products`         | Add a new product          | Product (JSON)       | Product details     |
| GET       | `/products/<id>`    | Get one product by ID      | —                    | Product details     |
| PUT       | `/products/<id>`    | Update product by ID       | Product (JSON)       | Updated product     |
| DELETE    | `/products/<id>`    | Delete product by ID       | —                    | Success message     |
| GET       | `/`                 | Health check endpoint      | —                    | Health status msg   |

All request/response payloads for product endpoints are validated & serialized with `ProductSchema`.

---

## SQLite Database Integration & Dependencies

- Uses SQLite for lightweight, file-based persistence.
- Database URL/path is defined by the environment variable `SQLITE_DB` (default: `sqlite:///products.db`).
- On startup, `init_db()` in `database.py` is called to initialize tables.
- All database interactions (CRUD) are handled through SQLAlchemy ORM in `services/product_service.py`.
- No SQL statements are handwritten—only ORM calls are used.

---

## Error Handling

- Custom error handlers (see `errors.py`) gracefully intercept validation errors (400), not found (404), and server errors (500).
- Error responses always follow a standardized JSON structure:
  ```json
  {
      "code": <number>,
      "status": "<status>",
      "message": "<description>",
      "errors": { ... }   // optional, for validation
  }
  ```
- All endpoints will provide appropriately accurate HTTP codes for error scenarios.

---

## OpenAPI & Documentation

- API schema is available in `interfaces/openapi.json`.
- API title, version, and endpoint metadata are presented for clients and can be consumed by Swagger UI (pre-configured in Flask settings).

---

## Environment Variables

- **SQLITE_DB**: Absolute or relative path to SQLite database file or URI (default: `sqlite:///products.db`).

---

## Extending the API

To add a new resource (e.g., Category):

1. Define a SQLAlchemy model in `models/`.
2. Create a Marshmallow schema in `schemas/`.
3. Add business logic/service in `services/`.
4. Write a controller using Flask-Smorest blueprint in `controllers/`.
5. Register the new blueprint under `routes/` and in `app/__init__.py`.
6. Handle any specific validation or custom errors in `errors.py` if needed.
7. Document the new endpoints in `interfaces/openapi.json` and update this documentation.

---

## Visual Architecture Diagram

```mermaid
flowchart LR
    subgraph Web Layer
        A[Flask App & Entry (run.py)] --> B[Routes (app/routes/)]
    end
    B --> C[Controllers (app/controllers/)]
    C --> D[Services (app/services/)]
    D --> E[Models (app/models/)]
    E <--> F[Database (app/database.py & SQLite)]
    C --> G[Schemas (app/schemas/)]
    G -. Marshmallow Validation .-> C
    A --> H[Error Handlers (app/errors.py)]
```

This diagram shows the high-level flow:  
- Entry point launches Flask app and sets up routes.
- Routes direct requests to controllers, which use schemas for (de-)serialization and call services for business logic.
- Services interact with the ORM models, which in turn read/write to the database.
- Errors are uniformly handled and routed back as JSON responses.

---
