## 1. User Registration


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

## 2. Place Creation


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

## 3. Review Submission


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

## 4. Fetching a List of Places


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
