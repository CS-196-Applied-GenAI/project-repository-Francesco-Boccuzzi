import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import enum


class StationStatus(str, enum.Enum):
    """Enum for station data collection status."""
    SUCCESS = "Success"
    NO_DATA = "No Data"
    PENDING = "Pending"


class Station(Base):
    """
    Database model for gas stations in São Paulo.
    Stores pricing, location, and verification information.
    """
    __tablename__ = "stations"

    # Primary identifier
    station_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    # Basic information
    name = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)  # E.164 format
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, default="São Paulo", index=True)

    # Location (coordinates)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)

    # Brand information
    bandeira = Column(String(100), nullable=False, index=True)

    # Price data
    gasolina_comum_price = Column(Float, nullable=True)

    # Tracking
    last_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Status
    status = Column(
        SQLEnum(StationStatus),
        default=StationStatus.PENDING,
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f"<Station(station_id={self.station_id}, name={self.name}, price={self.gasolina_comum_price})>"
