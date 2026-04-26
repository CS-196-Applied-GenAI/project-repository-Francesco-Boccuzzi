import pytest
import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from app.core.database import get_db
from app.models.station import Station, StationStatus
from main import app


# Test database setup - Use in-memory SQLite for tests
# We need to use String for UUID in SQLite instead of postgresql UUID type
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

# Create test base (separate from production)
TestBase = declarative_base()

# Import and re-declare Station model using String for UUID in tests
import uuid as uuid_module
from sqlalchemy import Column, String, Float, DateTime, Enum as SQLEnum

class StationModel(TestBase):
    """Test version of Station model using String for UUID."""
    __tablename__ = "stations"

    station_id = Column(String(36), primary_key=True, default=lambda: str(uuid_module.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, default="São Paulo", index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    bandeira = Column(String(100), nullable=False, index=True)
    gasolina_comum_price = Column(Float, nullable=True)
    last_verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    status = Column(
        SQLEnum(StationStatus),
        default=StationStatus.PENDING,
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f"<Station(station_id={self.station_id}, name={self.name}, price={self.gasolina_comum_price})>"

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    TestBase.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        TestBase.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_station_data():
    """Provide sample station data for testing."""
    return {
        "name": "Test Shell Station",
        "phone_number": "+551131234567",
        "address": "Rua Teste, 123, São Paulo, SP",
        "city": "São Paulo",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "bandeira": "Shell",
        "gasolina_comum_price": 5.89,
        "status": StationStatus.SUCCESS,
    }


@pytest.fixture
def multiple_stations_data():
    """Provide multiple station data for testing."""
    return [
        {
            "name": "Shell Av. Paulista",
            "phone_number": "+551131234567",
            "address": "Avenida Paulista, 1000, São Paulo, SP",
            "bandeira": "Shell",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "gasolina_comum_price": 5.89,
            "status": StationStatus.SUCCESS,
        },
        {
            "name": "Ipiranga Centro",
            "phone_number": "+551133567890",
            "address": "Rua 15 de Novembro, 250, São Paulo, SP",
            "bandeira": "Ipiranga",
            "latitude": -23.5504,
            "longitude": -46.6368,
            "gasolina_comum_price": 5.75,
            "status": StationStatus.SUCCESS,
        },
        {
            "name": "BR Vila Mariana",
            "phone_number": "+551138901234",
            "address": "Rua Brigadeiro, 567, São Paulo, SP",
            "bandeira": "BR",
            "latitude": -23.5873,
            "longitude": -46.6144,
            "gasolina_comum_price": 5.82,
            "status": StationStatus.PENDING,
        },
    ]
