from pydantic import BaseModel, Field, field_validator

class Family(BaseModel):
    family_id: int = Field(gt=0, le=2**12)
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=511)
    max_guests: int | None = Field(None, gt=0, le=20)
    can_host: bool = False
    family_members: list[int]
 
    @field_validator('name')
    @classmethod
    def name_must_not_be_whitespace(cls, v):
        if not v.strip():
            raise ValueError('name cannot be empty or whitespace only')
        return v.strip()

    @classmethod
    def from_dict(cls, data):
        """Create Family from dictionary."""
        return cls(**data)
    
    @classmethod
    def from_list(cls, data_list):
        """Create list of Family objects from data list."""
        return [cls.from_dict(data) for data in data_list]
