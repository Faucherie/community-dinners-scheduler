from pydantic import BaseModel, Field

# Configuration model
class Config(BaseModel):
    group_size: int = Field(gt=1, le=20) # ambiguous if referring to family or person
    group_size_family: int | None = Field(None, gt=0, le=10) # using group_size right now but should be more specific
    group_size_person: int | None = Field(None, gt=0, le=40) # using group_size right now but should be more specific
    events_per_series: int = Field(gt=0)
    series_count: int = Field(gt=0)

    @classmethod
    def from_dict(cls, data):
        """Create Config from dictionary."""
        return cls(**data)
