from fastapi import UploadFile
from io import BytesIO
import pandas as pd
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.models.record import Record
from app.schemas.record import RecordCreate
from app.utils.date_parser import parse_excel_datetime


EXCEL_COLUMN_MAP = {
    "PBM ID": "pbm_id",
    "description": "description",
    "create_date": "create_date",
    "status": "status",
    "owner": "owner",
    "info2": "info2",
}


def import_records_from_excel(file: UploadFile, db: Session):
    content = file.file.read()

    if file.filename.lower().endswith(".csv"):
        df = pd.read_csv(BytesIO(content))
    else:
        df = pd.read_excel(BytesIO(content))

    # 🔒 verificare coloane
    missing = [c for c in EXCEL_COLUMN_MAP if c not in df.columns]
    if missing:
        raise ValueError(f"Lipsesc coloane obligatorii: {missing}")

    created = 0
    skipped = []
    errors = []

    for idx, row in df.iterrows():
        try:
            raw_data = {}

            for excel_col, field in EXCEL_COLUMN_MAP.items():
                value = row.get(excel_col)

                # 🧹 curățare NaN / NaT
                if pd.isna(value):
                    value = None

                if field == "create_date" and value is not None:
                    value = parse_excel_datetime(value)

                raw_data[field] = value

            # 🔒 validare Pydantic
            record_in = RecordCreate(**raw_data)

            # 🔁 verificare PBM ID duplicat
            exists = (
                db.query(Record)
                .filter(Record.pbm_id == record_in.pbm_id)
                .first()
            )
            if exists:
                skipped.append({
                    "row": int(idx + 2),
                    "pbm_id": record_in.pbm_id,
                    "reason": "PBM ID existent",
                })
                continue

            record = Record(**record_in.model_dump())
            db.add(record)
            created += 1

        except ValidationError as ve:
            errors.append({
                "row": int(idx + 2),
                "error": ve.errors(),
            })

        except Exception as e:
            errors.append({
                "row": int(idx + 2),
                "error": str(e),
            })

    db.commit()

    return {
        "total_rows": int(len(df)),
        "created": int(created),
        "skipped": skipped,
        "errors": errors,
    }

