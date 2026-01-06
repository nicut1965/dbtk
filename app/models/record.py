from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    pbm_id = Column(Integer, unique=True, nullable=False, index=True)

    description = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

    status = Column(String, nullable=True)
    owner = Column(String, nullable=True)
    info2 = Column(Text, nullable=True)

