from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["medical", "water", "shelter", "other"]
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
