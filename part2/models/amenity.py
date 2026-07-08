"""Module For review"""


from basemodel import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, name):
        super().__init__()
        self.name = name
        if (not isinstance(self.name, str) or self.name.strip() == ""):
            raise ValueError("name cannot be embty")
        if (len(self.name) > 50):
            raise ValueError("maximum length for name is 50")
