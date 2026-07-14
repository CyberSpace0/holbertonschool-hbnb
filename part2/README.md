# HBnB Evolution — Part 2

## Business Logic and RESTful API

Part 2 of **HBnB Evolution** implements the backend business logic and exposes it through a RESTful API. The application is built with Python, Flask, and Flask-RESTX, and follows a layered architecture that separates the API, business logic, and persistence responsibilities.

The API manages four main resources:

- Users
- Amenities
- Places
- Reviews

Data is stored in memory through a repository abstraction, so it is reset whenever the application restarts.

## Architecture

The application is organized into three layers:

1. **Presentation layer** — Flask-RESTX namespaces and API endpoints.
2. **Business logic layer** — Domain models and the `HBnBFacade` service.
3. **Persistence layer** — Repository interface and in-memory implementation.

The Facade pattern provides a single entry point between the API layer and the application's models and repositories.

## Features

- Create, retrieve, list, and update users.
- Create, retrieve, list, and update amenities.
- Create, retrieve, list, and update places.
- Create, retrieve, list, update, and delete reviews.
- Associate places with owners and amenities.
- Associate reviews with users and places.
- Validate model attributes and resource relationships.
- Return appropriate HTTP status codes for invalid or missing resources.
- Generate interactive Swagger documentation automatically.
- Run automated unit and endpoint tests.
- Run manual black-box API tests with `cURL`.

## Project Structure

```text
part2/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── amenities.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── amenity.py
│   │   ├── basemodel.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   └── repository.py
│   └── services/
│       └── facade.py
├── test/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_models.py
├── TESTING_REPORT.md
├── curl_tests.sh
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## Requirements

- Python 3
- Flask
- Flask-RESTX

## Installation

Clone the repository and move to the Part 2 directory:

```bash
git clone <repository-url>
cd holbertonschool-hbnb/part2
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

From the `part2` directory, run:

```bash
python3 run.py
```

The development server starts at:

```text
http://127.0.0.1:5000
```

The interactive Swagger documentation is available at:

```text
http://127.0.0.1:5000/api/v1/
```

The generated OpenAPI document is available at:

```text
http://127.0.0.1:5000/swagger.json
```

## API Endpoints

The API base path is `/api/v1`.

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users/` | Create a user |
| `GET` | `/users/` | List all users |
| `GET` | `/users/<user_id>` | Retrieve a user |
| `PUT` | `/users/<user_id>` | Update a user |

### Amenities

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/amenities/` | Create an amenity |
| `GET` | `/amenities/` | List all amenities |
| `GET` | `/amenities/<amenity_id>` | Retrieve an amenity |
| `PUT` | `/amenities/<amenity_id>` | Update an amenity |

### Places

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/places/` | Create a place |
| `GET` | `/places/` | List all places |
| `GET` | `/places/<place_id>` | Retrieve a place |
| `PUT` | `/places/<place_id>` | Update a place |
| `GET` | `/places/<place_id>/reviews` | List reviews for a place |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/reviews/` | Create a review |
| `GET` | `/reviews/` | List all reviews |
| `GET` | `/reviews/<review_id>` | Retrieve a review |
| `PUT` | `/reviews/<review_id>` | Update a review |
| `DELETE` | `/reviews/<review_id>` | Delete a review |

## Request Examples

### Create a User

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ali",
    "last_name": "Ahmed",
    "email": "ali@example.com",
    "password": "secure-password"
  }'
```

### Create an Amenity

```bash
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Wi-Fi"}'
```

### Create a Place

Replace `<user_id>` and `<amenity_id>` with IDs returned by the API.

```bash
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Seaside Apartment",
    "description": "Apartment close to the beach",
    "price": 150.0,
    "latitude": 24.7136,
    "longitude": 46.6753,
    "owner_id": "<user_id>",
    "amenities": ["<amenity_id>"]
  }'
```

### Create a Review

Replace `<user_id>` and `<place_id>` with existing resource IDs.

```bash
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Excellent stay",
    "rating": 5,
    "user_id": "<user_id>",
    "place_id": "<place_id>"
  }'
```

## Validation Rules

| Resource | Main rules |
|---|---|
| User | Names are required and limited to 50 characters; email must be valid and unique |
| Amenity | Name is required and limited to 50 characters |
| Place | Title is required; price must be valid; latitude must be from `-90` to `90`; longitude must be from `-180` to `180`; owner and amenities must exist |
| Review | Text is required; rating must be an integer from `1` to `5`; user and place must exist |

Common response codes include:

- `200 OK` — Request completed successfully.
- `201 Created` — Resource created successfully.
- `400 Bad Request` — Invalid input or relationship.
- `404 Not Found` — Requested resource does not exist.

## Running the Automated Tests

From the `part2` directory, run:

```bash
python3 -m unittest discover -s test -v
```

The test suite covers model validation, API operations, boundary values, missing resources, invalid relationships, and Swagger availability.

## Running the cURL Tests

Start the Flask server first:

```bash
python3 run.py
```

Then, in another terminal, run:

```bash
bash curl_tests.sh
```

A detailed record of the test scope and results is available in [`TESTING_REPORT.md`](TESTING_REPORT.md).

## Persistence Note

Part 2 uses `InMemoryRepository`. All records exist only while the application process is running. Restarting the server clears the stored users, amenities, places, and reviews.

## Authors

- Azzam Al Duyuli
- Fahad Almidaj
- Ali Alsayah
