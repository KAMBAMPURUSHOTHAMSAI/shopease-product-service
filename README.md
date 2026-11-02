# ShopEase Product Service

An independent Product Management microservice built with **Python 3.11+, FastAPI, Pydantic, and Uvicorn**. It exposes REST APIs to create, retrieve, update, and delete products. Product data is stored in a Python dictionary in memory, as required by this training task; no database is used.

## 1. Features

- Create a product and generate a unique UUID product ID.
- Retrieve all products, with optional category filtering and pagination.
- Retrieve one product by ID.
- Update a product using `PUT` (all editable fields are sent in the request body).
- Delete a product.
- Validate request data with Pydantic.
- Return useful HTTP status codes for validation, invalid IDs, missing products, and unexpected errors.
- Interactive Swagger UI documentation.
- Docker image and container configuration.

> **Important:** In-memory data is temporary. All products are removed when the application process or container is restarted or recreated. This is intentional for this task.

## 2. Technology Stack

| Area | Technology |
|---|---|
| Language | Python 3.11+ |
| API framework | FastAPI |
| ASGI server | Uvicorn |
| Validation | Pydantic v2 |
| Configuration | Environment variables / python-dotenv |
| Containerization | Docker |
| API testing | Swagger UI / Postman |
| Version control | Git / GitHub |

## 3. Project Structure

```text
shopease-product-service/
├── app/
│   ├── main.py                    # Creates FastAPI app and registers routers/handlers
│   ├── routers/
│   │   └── product_routes.py      # Defines the five Product REST endpoints
│   ├── schemas/
│   │   └── product_schema.py      # Validates requests and defines response format
│   ├── models/
│   │   └── product_model.py       # Product data structure (dataclass)
│   ├── services/
│   │   └── product_service.py    # CRUD business logic and in-memory dictionary
│   └── config/
│       └── settings.py            # Reads application configuration
├── postman/
│   └── ShopEase_Product_Service.postman_collection.json
├── Dockerfile                     # Instructions to build the Docker image
├── .dockerignore                  # Excludes local/unneeded files from Docker context
├── .gitignore                     # Excludes local files from Git
├── .env                            # Local, non-secret development settings (do not commit)
├── .env.example                    # Safe configuration template
├── requirements.txt               # Python dependencies
└── README.md                       # Setup, API, Docker, and testing guide
```

### Responsibility of each application file

- **`main.py`:** Creates the FastAPI application, includes the Product router, provides health endpoints, and registers exception handlers.
- **`product_routes.py`:** Defines URL paths, HTTP methods, query/path parameters, request schemas, and response schemas. It delegates work to the service layer.
- **`product_schema.py`:** Defines Pydantic input/output models. It checks name, category, description, price, stock quantity, and status.
- **`product_model.py`:** Represents a product record in Python.
- **`product_service.py`:** Generates product IDs and implements create, list, get, update, and delete operations using an in-memory dictionary.
- **`settings.py`:** Reads app name, version, host, port, and debug settings from environment variables or local `.env`.

## 4. Run Locally on Windows

Open PowerShell or Command Prompt and move into the project directory:

```powershell
cd path\to\shopease-product-service
```

Verify Python:

```powershell
python --version
```

Create and activate a virtual environment in PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

For Command Prompt, activate with:

```bat
venv\Scripts\activate.bat
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the API locally:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8003
```

Open:

- Swagger UI: <http://127.0.0.1:8003/docs>
- ReDoc: <http://127.0.0.1:8003/redoc>
- Health check: <http://127.0.0.1:8003/health>

To save the exact installed dependency versions for your environment, you can run `pip freeze > requirements-lock.txt`. The supplied `requirements.txt` intentionally uses compatible version ranges.

## 5. Product API Endpoints

Base URL: `http://localhost:8003`

| Method | Endpoint | Purpose | Success status |
|---|---|---|---:|
| `POST` | `/api/products/` | Create a product | `201` |
| `GET` | `/api/products/` | List products | `200` |
| `GET` | `/api/products/{product_id}` | Get one product | `200` |
| `PUT` | `/api/products/{product_id}` | Replace editable product fields | `200` |
| `DELETE` | `/api/products/{product_id}` | Delete a product | `204` |

### Product JSON request body

Use this body for both `POST` and `PUT`:

```json
{
  "name": "Wireless Mouse",
  "description": "A comfortable wireless mouse",
  "price": 799.00,
  "stock_quantity": 25,
  "category": "Electronics",
  "status": "Active"
}
```

`description` is optional and `status` defaults to `Active`. Allowed status values are exactly `Active` and `Inactive`.

### List, filter, and pagination examples

```text
GET /api/products/
GET /api/products/?category=Electronics
GET /api/products/?skip=0&limit=10
GET /api/products/?category=Electronics&skip=0&limit=5
```

- `category`: optional, case-insensitive exact category match.
- `skip`: number of matching products to skip; default `0`.
- `limit`: maximum products to return; default `10`, allowed range `1` to `100`.

### Example successful response

```json
{
  "product_id": "9ddf6e2e-e9a6-43c1-9b2c-764e9fd40bfa",
  "name": "Wireless Mouse",
  "description": "A comfortable wireless mouse",
  "price": 799.0,
  "stock_quantity": 25,
  "category": "Electronics",
  "status": "Active",
  "created_at": "2026-11-02T05:00:00Z"
}
```

The example ID and timestamp are illustrative; the service generates real values.

## 6. Validation and Error Handling

| Condition | HTTP status | Meaning |
|---|---:|---|
| Successful read/update/delete | `200` / `204` | Request completed |
| Product created | `201` | New product created |
| Invalid UUID format in product ID | `400` | Product ID is malformed |
| Product does not exist | `404` | No matching product was found |
| Duplicate generated product ID | `409` | ID conflict (very unlikely with UUIDs) |
| Invalid body, missing field, wrong type, or constraint failure | `422` | Request validation failed |
| Unexpected server error | `500` | Generic internal error response |

Validation rules:

- Name: required, non-empty after trimming, maximum 100 characters.
- Description: optional, maximum 500 characters; blank text is stored as `null`.
- Price: required, finite number greater than zero.
- Stock quantity: required, integer greater than or equal to zero.
- Category: required, non-empty after trimming, maximum 50 characters.
- Status: only `Active` or `Inactive`.

## 7. Docker Instructions

Make sure Docker Desktop is installed and running. Run these commands from the project root.

Build the image:

```powershell
docker build -t shopease-product-service .
```

Check the image:

```powershell
docker images
```

Start the container and map host port `8003` to container port `8003`:

```powershell
docker run -d --name shopease-product-container -p 8003:8003 shopease-product-service
```

Check the running container and logs:

```powershell
docker ps
docker logs shopease-product-container
```

Open Swagger UI from the containerized application:

<http://localhost:8003/docs>

Health check:

<http://localhost:8003/health>

Container lifecycle commands:

```powershell
docker stop shopease-product-container
docker start shopease-product-container
docker rm -f shopease-product-container
```

To rebuild after changing source code, remove the old container, build the image again, and run a new container:

```powershell
docker rm -f shopease-product-container
docker build -t shopease-product-service .
docker run -d --name shopease-product-container -p 8003:8003 shopease-product-service
```

The Dockerfile starts Uvicorn on `0.0.0.0:8003`. Binding to `0.0.0.0` is necessary so that requests forwarded from the host can reach the process inside the container.

### Dockerfile instruction explanation

- `FROM python:3.11-slim`: starts from a compact Python 3.11 image.
- `ENV`: prevents Python bytecode files and makes logs appear immediately in Docker output.
- `WORKDIR /app`: sets the working directory inside the image.
- `COPY requirements.txt .`: copies dependency declarations first, improving Docker layer caching.
- `RUN pip install ...`: installs the Python packages into the image.
- `COPY app ./app`: copies the application source code.
- `RUN addgroup ...` and `USER appuser`: runs the service as a non-root user.
- `EXPOSE 8003`: documents the port used by the API; host access still requires `-p 8003:8003`.
- `CMD [...]`: starts Uvicorn when the container launches.

### Why `.dockerignore` matters

`.dockerignore` stops local virtual environments, Git metadata, cache files, temporary files, and `.env` from being sent in the Docker build context. The local `.env` is intentionally excluded so local configuration and possible secrets are not copied into the image. The application uses safe defaults inside Docker. Set container configuration through environment variables when needed, for example:

```powershell
docker run -d --name shopease-product-container -p 8003:8003 -e APP_NAME="ShopEase Product Service" shopease-product-service
```

## 8. API Testing Checklist

Test against the Docker-hosted service at `http://localhost:8003`, not only the local Uvicorn process.

1. `POST /api/products/` with the valid JSON above. Expect `201` and copy the returned `product_id`.
2. `POST /api/products/` with `"name": "   "`. Expect `422`.
3. `POST /api/products/` with `"price": -10`. Expect `422`.
4. `POST /api/products/` with `"stock_quantity": -1`. Expect `422`.
5. `GET /api/products/`. Expect `200` and a JSON array.
6. `GET /api/products/{copied_product_id}`. Expect `200` and the product.
7. `GET /api/products/not-a-uuid`. Expect `400`.
8. `GET /api/products/00000000-0000-4000-8000-000000000000`. Expect `404` if that ID has not been created.
9. `PUT /api/products/{copied_product_id}` with a valid complete product body. Expect `200`.
10. `GET /api/products/?category=Electronics`. Expect `200` with matching products only.
11. `GET /api/products/?skip=0&limit=1`. Expect no more than one product.
12. `DELETE /api/products/{copied_product_id}`. Expect `204` and an empty response body.
13. `GET /api/products/{copied_product_id}` after deletion. Expect `404`.

A ready-to-import Postman collection is available at `postman/ShopEase_Product_Service.postman_collection.json`. Import it into Postman, set `baseUrl` to `http://localhost:8003`, create a product first, and copy its returned ID into the `productId` collection variable before running get/update/delete requests.

## 9. Git and GitHub Submission

Initialize Git and commit the project:

```powershell
git init
git add .
git status
git commit -m "Build ShopEase Product CRUD microservice with Docker"
```

Create a GitHub repository named `shopease-product-service`, then connect and push it (replace the URL with your own repository URL):

```powershell
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shopease-product-service.git
git push -u origin main
```

Before pushing, confirm that `.env` is not staged or committed. The `.gitignore` excludes it. Never commit passwords, API keys, or private credentials.

## 10. Progress Update Template

Use this checklist for the team progress update:

- **Implementation completed:** FastAPI application, product CRUD, Pydantic validation, exception handlers.
- **Files created:** `app/main.py`, router, schema, model, service, settings, Dockerfile, `.dockerignore`, requirements, README.
- **APIs developed:** POST, GET all, GET by ID, PUT, DELETE.
- **Docker image:** Built / Not built (include image tag).
- **Docker container:** Running / Not running (include container name and port mapping).
- **Testing evidence:** Attach Swagger/Postman screenshots and successful/negative test results.
- **Issues and solutions:** Record the issue and the exact fix.
- **Pending tasks:** GitHub push, remaining tests, or demonstration items.

## 11. Important Concepts to Explain in Your Demonstration

1. A **client** (Swagger UI or Postman) sends an HTTP request to a URL.
2. FastAPI matches the HTTP method and URL to a route function in `product_routes.py`.
3. Pydantic validates the request body before the route function executes.
4. The route calls `product_service.py`, where the product dictionary is read or changed.
5. FastAPI serializes the returned product using `ProductResponse` and sends JSON with the correct status code.
6. Docker packages Python, dependencies, and application code into an image. A container runs that image in an isolated environment.

This implementation intentionally uses one independent service and in-memory storage. Database integration and communication with other microservices are outside the scope of this task.
