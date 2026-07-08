"""Module For review"""


from basemodel import BaseModel
from user import User
from place import Place

class Review(BaseModel):
    """Review class"""
    def __init__(self, text, rating, place, user):
        """initaillize function"""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        
        self.validate()
        
    def validate(self):
        """validate function"""
        if not isinstance(self.text, str) or self.text.strip() == "":
            raise ValueError("text is required")
        if not isinstance(self.rating, int) or (self.rating < 1 and self.rating > 5):
            raise ValueError("rating rquired between 1 and 5")
        if not isinstance(self.place, Place):
            raise ValueError("place must be instance Place")
        if not isinstance(self.user, User):
            raise ValueError("User must be instance User")
