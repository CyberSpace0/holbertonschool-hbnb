"""Module For Users"""
from app.models.basemodel import BaseModel

class User(BaseModel):
    """User class"""
    def __init__(self ,first_name, last_name, email, password=None, is_admin=False):
        """initailization function"""
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.validate()
        
    def validate(self):
        """validate function to ensure all attribaute is correct"""
        if not isinstance(self.first_name, str) or self.first_name.strip() == "":
            raise ValueError("first_name must be a non-empty string")

        if len(self.first_name) > 50:
            raise ValueError("first_name must be at most 50 characters")

        if not isinstance(self.last_name, str) or self.last_name.strip() == "":
            raise ValueError("last_name must be a non-empty string")

        if len(self.last_name) > 50:
            raise ValueError("last_name must be at most 50 characters")

        if not isinstance(self.email, str) or self.email.strip() == "":
            raise ValueError("email must be a non-empty string")

        if "@" not in self.email or "." not in self.email:
            raise ValueError("email must be a valid email")

        if not isinstance(self.password, str) or self.password.strip() == "":
            raise ValueError("password must be a non-empty string")

        if not isinstance(self.is_admin, bool):
            raise ValueError("is_admin must be a boolean")

    def updateProfile(self, data):
        self.update(data)
        self.validate()
