from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ProjectInquiry
from app.schemas.contact import ContactRequest, ContactResponse

router = APIRouter(prefix="/api", tags=["contact"])

@router.post("/contact", response_model=ContactResponse, status_code=status.HTTP_202_ACCEPTED)
async def contact(payload: ContactRequest, db: Session = Depends(get_db)):
    inquiry = ProjectInquiry(**payload.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return ContactResponse(message="Thanks — your project inquiry is ready for CodeShadow. We’ll use your details only to respond to this request.")
