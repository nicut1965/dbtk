from sqlalchemy import String, DateTime, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.database import Base

class Record(Base):
    __tablename__ = "records"

    pbm_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(String(50), index=True)

    create_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    close_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    submitter: Mapped[str] = mapped_column(String(255))
    owner: Mapped[str] = mapped_column(String(255))
    executor: Mapped[str] = mapped_column(String(255))

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    resolution: Mapped[str] = mapped_column(Text, nullable=True)

    info2: Mapped[str] = mapped_column(Text, nullable=True)

    @property
    def bmc(self) -> str:
        return f"https://bmc.company.local/pbm/{self.pbm_id}"
