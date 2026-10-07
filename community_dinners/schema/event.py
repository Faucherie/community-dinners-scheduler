# schema/event.py

from pydantic import BaseModel, Field, field_validator
from typing import List

class Event(BaseModel):
    event_id: int = Field(gt=0, le=2**12)
    host_family_id: int = Field(gt=0, le=2**12)
    guest_family_ids: List[int] = Field(min_length=1, max_length=50)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @field_validator('guest_family_ids')
    @classmethod
    def validate_guest_list(cls, v, info):
        # Check for invalid types (non-integers)
        for guest_id in v:
            if not isinstance(guest_id, int):
                raise ValueError(f'All guest IDs must be integers, got {type(guest_id).__name__}')
        
        # Check for negative IDs
        for guest_id in v:
            if guest_id <= 0:
                raise ValueError('Guest family IDs must be positive')
        
        # Check for empty list
        if len(v) == 0:
            raise ValueError('Event must have at least one guest family')
        
        # Check for host in guest list
        if 'host_family_id' in info.data and info.data['host_family_id'] in v:
            raise ValueError('Host family cannot be in the guest list')
        
        return v

