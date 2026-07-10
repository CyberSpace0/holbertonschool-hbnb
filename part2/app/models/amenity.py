"""Module For review"""


from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        if (not isinstance(self.name, str) or self.name.strip() == ""):
            raise ValueError("name cannot be embty")
        if (len(self.name) > 50):
            raise ValueError("maximum length for name is 50")

    def update(self, data):

        if "name" in data:
            self.name = data["name"]

        self.validate()
        self.save()