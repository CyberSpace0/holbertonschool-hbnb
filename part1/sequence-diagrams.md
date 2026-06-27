# Sequence Diagrams for API Calls

This document covers Task 2 of the HBnB technical documentation. The diagrams
show how the main API calls move through the Presentation Layer, Facade,
Business Logic Layer, Persistence Layer, and Database.

## Common Participants

- Client: the user or application sending the HTTP request.
- API: the Presentation Layer endpoint that receives and returns HTTP data.
- HBnBFacade: the facade that exposes a simple interface to the API layer.
- Business Logic: the models and validation rules for HBnB entities.
- Repository: the Persistence Layer abstraction used to store and retrieve data.
- Database: the final storage system.

## 1. User Registration

![Sequence Diagram - User Registration](<UML_Diagram/Sequence Diagram - User Registration.png>)

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as User API
    participant Facade as HBnBFacade
    participant UserModel as User Model
    participant Repo as User Repository
    participant DB as Database

    Client->>API: POST /api/v1/users
    API->>API: Validate request format and required fields
    API->>Facade: create_user(user_data)
    Facade->>Repo: get_by_email(email)
    Repo->>DB: Search user by email
    DB-->>Repo: Existing user or null
    Repo-->>Facade: Existing user or null

    alt Email already exists
        Facade-->>API: Email conflict error
        API-->>Client: 409 Conflict
    else Email is available
        Facade->>UserModel: Create User instance
        UserModel->>UserModel: Validate fields and protect password
        Facade->>Repo: save(user)
        Repo->>DB: Insert user record
        DB-->>Repo: Saved user
        Repo-->>Facade: User object
        Facade-->>API: User response data
        API-->>Client: 201 Created
    end
```

### Explanation

The client sends the registration data to the User API. The API checks that the
request is correctly formatted, then forwards the data to the `HBnBFacade`. The
facade checks that the email is not already used, creates a `User` object through
the Business Logic Layer, and stores it through the repository. If the operation
succeeds, the API returns a `201 Created` response.

## 2. Place Creation

![Sequence Diagram - Place Creation](<UML_Diagram/Sequence Diagram - Place Creation.png>)

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as Place API
    participant Facade as HBnBFacade
    participant PlaceModel as Place Model
    participant UserRepo as User Repository
    participant AmenityRepo as Amenity Repository
    participant PlaceRepo as Place Repository
    participant DB as Database

    Client->>API: POST /api/v1/places
    API->>API: Validate request and authenticated owner
    API->>Facade: create_place(owner_id, place_data)
    Facade->>UserRepo: get(owner_id)
    UserRepo->>DB: Select owner by id
    DB-->>UserRepo: Owner or null
    UserRepo-->>Facade: Owner or null

    alt Owner does not exist
        Facade-->>API: Owner validation error
        API-->>Client: 400 Bad Request
    else Owner exists
        Facade->>AmenityRepo: get_many(amenity_ids)
        AmenityRepo->>DB: Select requested amenities
        DB-->>AmenityRepo: Amenity records
        AmenityRepo-->>Facade: Amenity objects
        Facade->>PlaceModel: Create Place instance
        PlaceModel->>PlaceModel: Validate title, price, latitude, longitude
        Facade->>PlaceRepo: save(place)
        PlaceRepo->>DB: Insert place and place amenities
        DB-->>PlaceRepo: Saved place
        PlaceRepo-->>Facade: Place object
        Facade-->>API: Place response data
        API-->>Client: 201 Created
    end
```

### Explanation

The client sends the place details to the Place API. The API validates the
request and passes the data to the facade. The facade confirms that the owner
exists, loads the selected amenities, creates a `Place` object, validates the
business rules, and asks the repository to save the place. The API returns the
created place when storage succeeds.

## 3. Review Submission

![Sequence Diagram - Review Submission](<UML_Diagram/Sequence Diagram - Review Submission.png>)

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as Review API
    participant Facade as HBnBFacade
    participant ReviewModel as Review Model
    participant PlaceRepo as Place Repository
    participant UserRepo as User Repository
    participant ReviewRepo as Review Repository
    participant DB as Database

    Client->>API: POST /api/v1/places/{place_id}/reviews
    API->>API: Validate request and authenticated user
    API->>Facade: create_review(place_id, user_id, review_data)
    Facade->>PlaceRepo: get(place_id)
    PlaceRepo->>DB: Select place by id
    DB-->>PlaceRepo: Place or null
    PlaceRepo-->>Facade: Place or null

    alt Place does not exist
        Facade-->>API: Place not found
        API-->>Client: 404 Not Found
    else Place exists
        Facade->>UserRepo: get(user_id)
        UserRepo->>DB: Select user by id
        DB-->>UserRepo: User or null
        UserRepo-->>Facade: User or null

        alt User does not exist
            Facade-->>API: User validation error
            API-->>Client: 400 Bad Request
        else User exists
            Facade->>ReviewModel: Create Review instance
            ReviewModel->>ReviewModel: Validate rating and comment
            Facade->>ReviewRepo: save(review)
            ReviewRepo->>DB: Insert review record
            DB-->>ReviewRepo: Saved review
            ReviewRepo-->>Facade: Review object
            Facade-->>API: Review response data
            API-->>Client: 201 Created
        end
    end
```

### Explanation

The client submits a review for a specific place. The API validates the request
and sends the place id, user id, and review data to the facade. The facade checks
that the place and user exist, then creates and validates the `Review` object.
The repository stores the review, and the API returns the created review data.

## 4. Fetching a List of Places

![Sequence Diagram - Fetching Places](<UML_Diagram/Sequence Diagram - Fetching Places.png>)

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant API as Place API
    participant Facade as HBnBFacade
    participant PlaceModel as Place Model
    participant PlaceRepo as Place Repository
    participant DB as Database

    Client->>API: GET /api/v1/places?filters
    API->>API: Parse pagination and filter parameters
    API->>Facade: get_places(filters)
    Facade->>PlaceRepo: list(filters)
    PlaceRepo->>DB: Query places with filters
    DB-->>PlaceRepo: Matching place records
    PlaceRepo-->>Facade: Place objects
    Facade->>PlaceModel: Format place data for response
    PlaceModel-->>Facade: Place response DTOs
    Facade-->>API: List of places
    API-->>Client: 200 OK
```

### Explanation

The client requests a list of places, optionally using filters such as location,
price, or pagination. The API parses the query parameters and calls the facade.
The facade requests the matching places from the repository, which queries the
database. The results are returned to the API as response data, and the client
receives a `200 OK` response with a list of places.

## Design Notes

- The API layer only handles HTTP input and output.
- The `HBnBFacade` centralizes the main application operations and keeps the API
  from directly depending on repository details.
- The Business Logic Layer is responsible for entity rules such as required
  fields, valid ratings, valid prices, and valid coordinates.
- The Persistence Layer hides the storage implementation behind repositories.
- These diagrams focus on the main success paths while also showing important
  validation failures where they affect the API response.
