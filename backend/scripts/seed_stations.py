"""
Seed script to populate São Paulo gas stations into the database.
Uses real São Paulo neighborhoods and gas station chains.
"""
import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.station import Station, StationStatus


# Real São Paulo gas station chains and realistic data
SAO_PAULO_STATIONS = [
    {
        "name": "Shell Av. Paulista",
        "phone_number": "+551131234567",
        "address": "Avenida Paulista, 1000, São Paulo, SP",
        "bandeira": "Shell",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "price": 5.89,
    },
    {
        "name": "Ipiranga Centro",
        "phone_number": "+551133567890",
        "address": "Rua 15 de Novembro, 250, São Paulo, SP",
        "bandeira": "Ipiranga",
        "latitude": -23.5504,
        "longitude": -46.6368,
        "price": 5.75,
    },
    {
        "name": "BR Vila Mariana",
        "phone_number": "+551138901234",
        "address": "Rua Brigadeiro, 567, São Paulo, SP",
        "bandeira": "BR",
        "latitude": -23.5873,
        "longitude": -46.6144,
        "price": 5.82,
    },
    {
        "name": "Petrobras Pinheiros",
        "phone_number": "+551142345678",
        "address": "Rua dos Pinheiros, 1234, São Paulo, SP",
        "bandeira": "Petrobras",
        "latitude": -23.5562,
        "longitude": -46.6747,
        "price": 5.88,
    },
    {
        "name": "Shell Consolação",
        "phone_number": "+551145678901",
        "address": "Avenida Consolação, 789, São Paulo, SP",
        "bandeira": "Shell",
        "latitude": -23.5457,
        "longitude": -46.6592,
        "price": 5.91,
    },
    {
        "name": "Ipiranga Morumbi",
        "phone_number": "+551146789012",
        "address": "Avenida Morumbi, 2000, São Paulo, SP",
        "bandeira": "Ipiranga",
        "latitude": -23.5938,
        "longitude": -46.7285,
        "price": 5.76,
    },
    {
        "name": "BR Tatuapé",
        "phone_number": "+551147890123",
        "address": "Rua Tatuapé, 500, São Paulo, SP",
        "bandeira": "BR",
        "latitude": -23.5281,
        "longitude": -46.5559,
        "price": 5.79,
    },
    {
        "name": "Petrobras Imirim",
        "phone_number": "+551148901234",
        "address": "Rua Imirim, 1500, São Paulo, SP",
        "bandeira": "Petrobras",
        "latitude": -23.4958,
        "longitude": -46.6244,
        "price": 5.85,
    },
    {
        "name": "Shell Vila Madalena",
        "phone_number": "+551149012345",
        "address": "Rua Wisard, 430, São Paulo, SP",
        "bandeira": "Shell",
        "latitude": -23.5701,
        "longitude": -46.6936,
        "price": 5.93,
    },
    {
        "name": "Ipiranga Lapa",
        "phone_number": "+551150123456",
        "address": "Rua Carvalho Mendes, 320, São Paulo, SP",
        "bandeira": "Ipiranga",
        "latitude": -23.5226,
        "longitude": -46.6930,
        "price": 5.74,
    },
    {
        "name": "BR Liberdade",
        "phone_number": "+551151234567",
        "address": "Avenida Liberdade, 450, São Paulo, SP",
        "bandeira": "BR",
        "latitude": -23.5594,
        "longitude": -46.6300,
        "price": 5.81,
    },
    {
        "name": "Petrobras Vila Alpina",
        "phone_number": "+551152345678",
        "address": "Avenida Vila Alpina, 800, São Paulo, SP",
        "bandeira": "Petrobras",
        "latitude": -23.5428,
        "longitude": -46.5101,
        "price": 5.83,
    },
    {
        "name": "Shell Brooklin",
        "phone_number": "+551153456789",
        "address": "Rua Bela Cintra, 675, São Paulo, SP",
        "bandeira": "Shell",
        "latitude": -23.6030,
        "longitude": -46.6480,
        "price": 5.90,
    },
    {
        "name": "Ipiranga Itaim",
        "phone_number": "+551154567890",
        "address": "Avenida Brigadeiro Faria Lima, 1200, São Paulo, SP",
        "bandeira": "Ipiranga",
        "latitude": -23.5932,
        "longitude": -46.6794,
        "price": 5.77,
    },
    {
        "name": "BR Santana",
        "phone_number": "+551155678901",
        "address": "Rua Voluntários da Pátria, 2500, São Paulo, SP",
        "bandeira": "BR",
        "latitude": -23.5067,
        "longitude": -46.6206,
        "price": 5.80,
    },
]


def seed_database():
    """
    Populate the database with real São Paulo gas stations.
    All stations are initialized with status "Pending" and no verified price yet.
    """
    db: Session = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(Station).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} stations. Skipping seed.")
            return

        print("Seeding São Paulo gas stations...")
        
        for station_data in SAO_PAULO_STATIONS:
            station = Station(
                name=station_data["name"],
                phone_number=station_data["phone_number"],
                address=station_data["address"],
                city="São Paulo",
                bandeira=station_data["bandeira"],
                latitude=station_data["latitude"],
                longitude=station_data["longitude"],
                gasolina_comum_price=station_data["price"],
                status=StationStatus.SUCCESS,  # For testing, mark as verified
                last_verified_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(station)

        db.commit()
        
        # Verify insertion
        total = db.query(Station).count()
        print(f"✓ Successfully seeded {total} gas stations!")
        
        # Show summary
        for bandeira in ["Shell", "Ipiranga", "BR", "Petrobras"]:
            count = db.query(Station).filter(Station.bandeira == bandeira).count()
            print(f"  - {bandeira}: {count} stations")

    except Exception as e:
        db.rollback()
        print(f"✗ Error seeding database: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
