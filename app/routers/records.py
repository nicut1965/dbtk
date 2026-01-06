from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordRead

router = APIRouter()


@router.post("/records", response_model=RecordRead)
def create_record(
    record: RecordCreate,
    db: Session = Depends(get_db)
):
    db_record = Record(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
