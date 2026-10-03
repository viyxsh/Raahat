from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ticket
from ..schemas import TicketList, TicketOut, TicketUpdate

router = APIRouter()

URGENCY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


@router.get("/requests", response_model=TicketList)
def list_requests(db: Session = Depends(get_db)):
    """Tickets sorted by urgency rank, then newest first within the same
    urgency level. Unclassified tickets sort last."""
    tickets = (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc(), Ticket.id.desc())
        .all()
    )
    tickets.sort(key=lambda t: URGENCY_RANK.get(t.urgency, 4))
    return {"tickets": tickets}


@router.get("/requests/{ticket_id}", response_model=TicketOut)
def get_request(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    return ticket


@router.patch("/requests/{ticket_id}", response_model=TicketOut)
def update_request(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    """The classifier sets category and urgency, the coordinator dashboard
    moves status along."""
    ticket = db.get(Ticket, ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="ticket not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket
