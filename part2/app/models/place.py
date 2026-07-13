"""Module For place"""


from app.models.user import User
from app.models.basemodel import BaseModel


class Place(BaseModel):
    def __init__(self,title,price,latitude,longitude,owner,description=""):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
      
        self.reviews = []
        self.amenities = []
        self.validate()

    def validate(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title must be a non-empty string")

        if len(self.title) > 100:
            raise ValueError("title must be at most 100 characters")

        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("description must be a string")

        if not isinstance(self.price, (int, float)):
            raise ValueError("price must be a number")

        if self.price < 0:
            raise ValueError("price must be non-negative")

        if not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number")

        if not -90 <= self.latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")

        if not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number")

        if not -180 <= self.longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")

        if not isinstance(self.owner, User):
            raise ValueError("owner must be a User")
    
    def add_review(self, review):
        self.reviews.append(review)
        self.save()
        
    def add_amenities(self, amenity):
        self.amenities.append(amenity)
        self.save()

    def remove_review(self, review):
        if (review in self.reviews):
            self.reviews.remove(review)
            self.save()
    
    def remove_amenities(self, amenity):
        if (amenity in self.amenities):
            self.amenities.remove(amenity)

    def updatePlace(self, data):
        self.update(data)
        self.validate()
