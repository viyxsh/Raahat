import sys
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from classifier.classifier import classify

from ..database import get_db
from ..models import Ticket
from ..schemas import TicketCreate, TicketOut

router = APIRouter()


@router.post("/simulate/sms", response_model=TicketOut, status_code=201)
def simulate_sms(payload: TicketCreate, db: Session = Depends(get_db)):
    """Stores a fake inbound SMS as a ticket, the same way a real SMS gateway
    webhook will once one is connected. The classifier runs before the ticket
    is committed, so every request arrives at humans already understood."""
    result = classify(payload.message)
    ticket = Ticket(
        text=payload.message,
        phone=payload.phone,
        lat=payload.lat,
        lng=payload.lng,
        category=result["category"],
        urgency=result["urgency"],
        status="flagged" if result["is_duplicate"] else "new",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
