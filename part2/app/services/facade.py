from app.models.place import Place
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    def get_alluser(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        """Updates user data. Returns the updated user or None if not found"""
        return self.user_repo.update(user_id,user_data)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None

        amenity.update(amenity_data)
        return amenity

    def create_place(self, place_data):
        owner_id = place_data.pop("owner_id", None)
        owner = self.get_user(owner_id)

        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.pop("amenities", [])
        amenities = []

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")
            amenities.append(amenity)

        place = Place(owner=owner, **place_data)

        for amenity in amenities:
            place.add_amenities(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)

        if not place:
            return None

        return place.reviews

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)

        if not place:
            return None

        if "owner_id" in place_data:
            owner = self.get_user(place_data.pop("owner_id"))
            if not owner:
                raise ValueError("Owner not found")
            place.owner = owner

        if "amenities" in place_data:
            amenity_ids = place_data.pop("amenities")
            place.amenities = []

            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError("Amenity not found")
                place.add_amenities(amenity)

        place.update(place_data)
        place.validate()
        return place

    def create_review(self, review_data):
    # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        rev = Review(**review_data)
        self.review_repo.add(rev)
        return rev

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        ## Placeholder for logic to retrieve all reviews
        #x = User("aa","dd","daf@gmail.com","21441Aa32")
        #print(x.__dict__)
        #xx = Place("workspace",500,24,11,x,"test only")
        #print(xx.__dict__)
        #self.user_repo.add(x)
        #self.place_repo.add(xx)
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        return self.review_repo.get_by_attribute("place",place_id)

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        return self.review_repo.delete(review_id)