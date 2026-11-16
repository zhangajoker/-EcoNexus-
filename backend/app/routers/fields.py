"""Field nodes (digital-twin plots)."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FieldNode

router = APIRouter(prefix="/api", tags=["fields"])


@router.get("/fields")
def get_all_fields(db: Session = Depends(get_db)):
    return db.query(FieldNode).all()
