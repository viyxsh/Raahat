from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ticket
from ..schemas import TicketCreate, TicketOut

router = APIRouter()


@router.post("/simulate/sms", response_model=TicketOut, status_code=201)
def simulate_sms(payload: TicketCreate, db: Session = Depends(get_db)):
    """Stores a fake inbound SMS as a ticket, the same way a real SMS gateway
    webhook will once one is connected."""
    ticket = Ticket(
        text=payload.message, phone=payload.phone, lat=payload.lat, lng=payload.lng
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
