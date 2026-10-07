from pydantic import BaseModel, Field
 
# Data models
class Person(BaseModel):
    # Required fields
    person_id: int = Field(gt=0, le=2**12)
    first_name: str = Field(max_length=255)
    last_name: str = Field(max_length=255)
    
    # Optional fields
    family_id: int | None = None
    age: int | None = Field(default=None, gt=0, le=150)
    kid: bool = False
    phone: str = ""
    email: str = ""
 
    @classmethod
    def from_dict(cls, data):
        """Create Person from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_list(cls, data_list):
        """Create list of Person objects from data list."""
        return [cls.from_dict(data) for data in data_list]