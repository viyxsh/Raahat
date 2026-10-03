from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# "food" is a valid classifier output (the rule engine has food keywords) even
# though the prototype schema exposes the four categories the team agreed on
Category = Literal["medical", "water", "shelter", "food", "other"]
Urgency = Literal["low", "medium", "high", "critical"]
TicketStatus = Literal["new", "flagged", "verified", "assigned"]


class TicketCreate(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    phone: str = Field(min_length=5, max_length=20)
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)


class TicketUpdate(BaseModel):
    category: Category | None = None
    urgency: Urgency | None = None
    status: TicketStatus | None = None

    @field_validator("status", mode="before")
    @classmethod
    def status_cannot_be_null(cls, v):
        # status is non-nullable in the DB, so an explicit null must be
        # rejected here with a 422 instead of failing on commit with a 500
        if v is None:
            raise ValueError("status cannot be set to null")
        return v


class TicketOut(BaseModel):
    id: int
    text: str
    phone: str
    lat: float
    lng: float
    category: Category | None
    urgency: Urgency | None
    status: TicketStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class TicketList(BaseModel):
    tickets: list[TicketOut]
