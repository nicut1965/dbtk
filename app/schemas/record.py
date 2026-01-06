from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# -------------------------
# Baza comuna
# -------------------------
class RecordBase(BaseModel):
    pbm_id: int = Field(..., description="PBM ID numeric, unic")
    description: str = Field(..., description="Descriere la creare")
    create_date: datetime = Field(..., description="Data creare (din Excel)")
    status: Optional[str] = None
    owner: Optional[str] = None
    info2: Optional[str] = None


# -------------------------
# La creare / import
# -------------------------
class RecordCreate(RecordBase):
    pass


# -------------------------
# La citire (API response)
# -------------------------
class RecordRead(RecordBase):
    id: int

    model_config = {
        "from_attributes": True
    }
