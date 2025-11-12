from pydantic import BaseModel, Field, validator
from typing import Optional


class Feedback(BaseModel):
    name: str = Field(..., min_length=1)
    contact: str = Field(..., min_length=1)
    shopping_rating: int = Field(..., ge=1, le=5, description="1-5 rating")
    items_not_found: Optional[str] = None
    price_reduction_items: Optional[str] = None
    improvement_suggestions: Optional[str] = None

    @validator("contact")
    def contact_must_be_reasonable(cls, v):
        # Basic length check for contact info
        if len(v) != 11:
            raise ValueError("Contact information is invalid")
