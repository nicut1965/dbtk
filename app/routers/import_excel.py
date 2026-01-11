from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.core.dependencies import get_current_user
from app.database import get_db
from app.services.excel_import import import_records_from_excel

router = APIRouter()


@router.post("/import/excel")
def import_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    #current_user = Depends(get_current_user)
):
    return import_records_from_excel(file, db)
