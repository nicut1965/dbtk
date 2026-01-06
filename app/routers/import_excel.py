from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.excel_import import import_records_from_excel

router = APIRouter()


@router.post("/import/excel")
def import_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return import_records_from_excel(file, db)
