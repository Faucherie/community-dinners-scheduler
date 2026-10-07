from pydantic import BaseModel, Field
from typing import List
 
class Series(BaseModel):
    series_id: int = Field(gt=0)
    event_ids: List[int] = Field(min_length=1)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)