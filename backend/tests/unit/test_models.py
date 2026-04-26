"""
Tests for Station model and database operations.
Covers CRUD operations, validation, and edge cases.
"""
import pytest
from datetime import datetime, timedelta
from typing import cast
from sqlalchemy.exc import IntegrityError
from tests.conftest import StationModel, StationStatus


class TestStationCreation:
    """Test Station model creation and basic properties."""

    def test_create_station_with_all_fields(self, db, sample_station_data):
        """Test creating a station with all required fields."""
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).filter_by(name="Test Shell Station").first()
        assert retrieved is not None
        assert retrieved.name == "Test Shell Station"
        assert retrieved.bandeira == "Shell"
        assert retrieved.gasolina_comum_price == 5.89
        assert retrieved.latitude == -23.5505
        assert retrieved.longitude == -46.6333
        assert retrieved.status == StationStatus.SUCCESS

    def test_station_id_auto_generated(self, db, sample_station_data):
        """Test that station_id is automatically generated."""
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        assert station.station_id is not None
        assert isinstance(station.station_id, str)

    def test_create_station_with_null_price(self, db, sample_station_data):
        """Test creating a station with null price."""
        sample_station_data["gasolina_comum_price"] = None
        sample_station_data["status"] = StationStatus.PENDING
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.gasolina_comum_price is None
        assert retrieved.status == StationStatus.PENDING

    def test_create_station_no_data_status(self, db, sample_station_data):
        """Test creating a station with NO_DATA status."""
        sample_station_data["status"] = StationStatus.NO_DATA
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.status == StationStatus.NO_DATA

    def test_station_city_defaults_to_sao_paulo(self, db):
        """Test that city defaults to São Paulo."""
        station = StationModel(
            name="Test Station",
            phone_number="+551131234567",
            address="Rua Teste, 123",
            latitude=-23.5505,
            longitude=-46.6333,
            bandeira="Shell",
        )
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.city == "São Paulo"

    def test_station_status_defaults_to_pending(self, db):
        """Test that status defaults to PENDING."""
        station = StationModel(
            name="Test Station",
            phone_number="+551131234567",
            address="Rua Teste, 123",
            city="São Paulo",
            latitude=-23.5505,
            longitude=-46.6333,
            bandeira="Shell",
        )
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.status == StationStatus.PENDING


class TestStationValidation:
    """Test required fields and validation."""

    def test_name_required(self, db):
        """Test that name field is required."""
        station = StationModel(
            phone_number="+551131234567",
            address="Rua Teste, 123",
            city="São Paulo",
            latitude=-23.5505,
            longitude=-46.6333,
            bandeira="Shell",
        )
        db.add(station)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_phone_required(self, db):
        """Test that phone_number field is required."""
        station = StationModel(
            name="Test Station",
            address="Rua Teste, 123",
            city="São Paulo",
            latitude=-23.5505,
            longitude=-46.6333,
            bandeira="Shell",
        )
        db.add(station)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_coordinates_required(self, db):
        """Test that latitude and longitude are required."""
        station = StationModel(
            name="Test Station",
            phone_number="+551131234567",
            address="Rua Teste, 123",
            city="São Paulo",
            bandeira="Shell",
        )
        db.add(station)
        with pytest.raises(IntegrityError):
            db.commit()

    def test_e164_phone_format(self, db, sample_station_data):
        """Test that phone numbers are in E.164 format."""
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.phone_number.startswith("+55")
        assert len(retrieved.phone_number) >= 13


class TestStationEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_extreme_latitude_south_pole(self, db, sample_station_data):
        """Test station with extreme latitude."""
        sample_station_data["latitude"] = -90.0
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.latitude == -90.0

    def test_extreme_longitude(self, db, sample_station_data):
        """Test station with extreme longitude."""
        sample_station_data["longitude"] = 180.0
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.longitude == 180.0

    def test_price_zero(self, db, sample_station_data):
        """Test station with zero price."""
        sample_station_data["gasolina_comum_price"] = 0.0
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.gasolina_comum_price == 0.0

    def test_price_very_high(self, db, sample_station_data):
        """Test station with very high price."""
        sample_station_data["gasolina_comum_price"] = 999.99
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.gasolina_comum_price == 999.99

    def test_last_verified_timestamp(self, db, sample_station_data):
        """Test setting last_verified_at timestamp."""
        test_time = datetime.utcnow() - timedelta(days=5)
        sample_station_data["last_verified_at"] = test_time
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        retrieved = db.query(StationModel).first()
        assert retrieved.last_verified_at == test_time


class TestStationTimestamps:
    """Test automatic timestamp management."""

    def test_created_at_auto_set(self, db, sample_station_data):
        """Test that created_at is automatically set."""
        before = datetime.utcnow()
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()
        after = datetime.utcnow()

        assert station.created_at is not None
        assert before.timestamp() <= station.created_at.timestamp() <= after.timestamp()

    def test_updated_at_auto_set(self, db, sample_station_data):
        """Test that updated_at is automatically set."""
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        assert station.updated_at is not None




class TestStationQuerying:
    """Test querying and filtering stations."""

    def test_query_by_name(self, db, multiple_stations_data):
        """Test querying station by name."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        station = db.query(StationModel).filter_by(name="Shell Av. Paulista").first()
        assert station is not None
        assert station.name == "Shell Av. Paulista"

    def test_query_by_brand(self, db, multiple_stations_data):
        """Test querying stations by brand."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        stations = db.query(StationModel).filter_by(bandeira="Shell").all()
        assert len(stations) == 1

    def test_query_by_status(self, db, multiple_stations_data):
        """Test querying stations by status."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        pending = db.query(StationModel).filter_by(status=StationStatus.PENDING).all()
        assert len(pending) == 1

    def test_count_all_stations(self, db, multiple_stations_data):
        """Test counting all stations."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        count = db.query(StationModel).count()
        assert count == 3

    def test_sort_by_price(self, db, multiple_stations_data):
        """Test querying stations sorted by price."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        stations = db.query(StationModel).order_by(StationModel.gasolina_comum_price).all()
        assert stations[0].gasolina_comum_price == 5.75
        assert stations[2].gasolina_comum_price == 5.89

    def test_find_cheapest(self, db, multiple_stations_data):
        """Test finding the cheapest station."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        cheapest = db.query(StationModel).order_by(StationModel.gasolina_comum_price).first()
        assert cheapest.gasolina_comum_price == 5.75

    def test_query_no_results(self, db):
        """Test querying with no results."""
        result = db.query(StationModel).filter_by(name="NonExistent").first()
        assert result is None


class TestStationUpdates:
    """Test updating station records."""

    def test_update_status(self, db, sample_station_data):
        """Test updating station status."""
        sample_station_data["status"] = StationStatus.PENDING
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        # Use a type ignore to bypass Pylance's strict check on this line
        station.status = StationStatus.NO_DATA  # type: ignore
        db.commit()

        retrieved = db.query(StationModel).first()
        
        # Use 'is' for Enum comparison or wrap in bool() to avoid 'NoReturn' errors
        assert retrieved.status is StationStatus.NO_DATA

    def test_bulk_update_statuses(self, db, multiple_stations_data):
        """Test bulk updating all stations."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        db.query(StationModel).update({StationModel.status: StationStatus.SUCCESS})
        db.commit()

        updated = db.query(StationModel).filter_by(status=StationStatus.SUCCESS).all()
        assert len(updated) == 3


class TestStationDeletion:
    """Test deleting station records."""

    def test_delete_station(self, db, sample_station_data):
        """Test deleting a station."""
        station = StationModel(**sample_station_data)
        db.add(station)
        db.commit()

        station_id = station.station_id
        db.delete(station)
        db.commit()

        retrieved = db.query(StationModel).filter_by(station_id=station_id).first()
        assert retrieved is None

    def test_delete_multiple(self, db, multiple_stations_data):
        """Test deleting multiple stations."""
        for data in multiple_stations_data:
            db.add(StationModel(**data))
        db.commit()

        db.query(StationModel).filter_by(bandeira="Shell").delete()
        db.commit()

        remaining = db.query(StationModel).count()
        assert remaining == 2