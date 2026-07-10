"""Amenity model"""

from app.models.basemodel import BaseModel


class Amenity(BaseModel):
    """Amenity class"""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.validate()

    def validate(self):
        """Validate amenity attributes"""
        if not isinstance(self.name, str) or self.name.strip() == "":
            raise ValueError("name cannot be empty")

        if len(self.name) > 50:
            raise ValueError("maximum length for name is 50")

    def update(self, data):
        """Update amenity attributes"""
        if "name" in data:
            self.name = data["name"]

        self.validate()
        self.save()
