import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel defines common attributes/methods
    for all models in the application.
    """

    def __init__(self, **kwargs):
        """
        Initialize a new model instance
        """

        self.id = kwargs.get("id", str(uuid.uuid4()))
        self.created_at = kwargs.get("created_at", datetime.now().timestamp())
        self.updated_at = kwargs.get("updated_at", datetime.now().timestamp())

    def save(self):
        """
        Updates the updated_at timestamp
        """
        self.updated_at = datetime.now().timestamp()

    def to_dict(self):
       return {
           "id": self.id,
           "created_at": self.created_at.isoformat(),
           "updated_at": self.updated_at.isoformat()
       }