import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import String, Float, DateTime, Enum as SQLEnum, TypeDecorator, CHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from app.core.database import Base
import enum

# --- Platform Independent UUID Helper ---
class GUID(TypeDecorator):
    """
    Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses CHAR(36) for SQLite.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return uuid.UUID(value)


class StationStatus(str, enum.Enum):
    SUCCESS = "Success"
    NO_DATA = "No Data"
    PENDING = "Pending"


class Station(Base):
    __tablename__ = "stations"

    # Primary identifier - Uses the GUID helper for SQLite compatibility
    station_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    # Basic information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, default="São Paulo", index=True)

    # Location
    latitude: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=False, index=True)

    # Brand
    bandeira: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Price data - Optional[float] handles nullable=True for the type checker
    gasolina_comum_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Tracking
    # Note: utcnow is deprecated in Python 3.12+, using timezone-aware UTC is safer
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    # Status
    status: Mapped[StationStatus] = mapped_column(
        SQLEnum(StationStatus),
        default=StationStatus.PENDING,
        nullable=False,
        index=True
    )

    def __repr__(self) -> str:
        return f"<Station(station_id={self.station_id}, name={self.name}, price={self.gasolina_comum_price})>"