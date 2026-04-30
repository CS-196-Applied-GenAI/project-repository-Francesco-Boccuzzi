"""
API routes for station management and spatial queries.

This module implements Phase 2 of the development plan:
- Step 2.1: Spatial Query Endpoint (GET /api/stations)
- Step 2.2: Admin Override API (PATCH /api/stations/:id)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.core.database import get_db
from app.models.station import Station, StationStatus
from app.schemas import (
    SearchQuery,
    StationResponse,
    StationUpdate,
    StationListResponse,
)
from app.utils import filter_stations_by_radius

# Create router for station endpoints
router = APIRouter(prefix="/api/stations", tags=["stations"])


@router.get("", response_model=StationListResponse)
def search_stations(
    latitude: float = Query(..., ge=-90, le=90, description="Search center latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Search center longitude"),
    radius_km: float = Query(default=2.0, ge=1.0, le=5.0, description="Search radius in kilometers"),
    db: Session = Depends(get_db),
):
    """
    Search for gas stations within a specified radius.
    
    **Phase 2.1 Implementation:**
    - Accepts latitude, longitude, and radius (1-5km)
    - Returns all stations within the radius using Haversine distance calculation
    - Calculates distance for each station
    - Identifies and returns the cheapest station ID
    
    Query Parameters:
        - latitude: Center search point latitude (-90 to 90)
        - longitude: Center search point longitude (-180 to 180)
        - radius_km: Search radius in kilometers (1-5, default 2)
    
    Returns:
        StationListResponse containing:
        - stations: List of stations within radius (sorted by distance)
        - count: Number of results
        - cheapest_station_id: UUID of cheapest station
        - search_center: Coordinates used for search
        - search_radius_km: Radius used for search
    """
    # Fetch all stations from database
    all_stations = db.query(Station).all()
    
    # Filter stations by radius using Haversine formula
    nearby_stations = filter_stations_by_radius(
        all_stations,
        center_lat=latitude,
        center_lon=longitude,
        radius_km=radius_km
    )
    
    # Build response models with calculated distance
    station_responses = []
    cheapest_station_id = None
    cheapest_price = float('inf')
    
    for station in nearby_stations:
        station_response = StationResponse(
            station_id=str(station.station_id),
            name=station.name,
            phone_number=station.phone_number,
            address=station.address,
            city=station.city,
            latitude=station.latitude,
            longitude=station.longitude,
            bandeira=station.bandeira,
            gasolina_comum_price=station.gasolina_comum_price,
            status=station.status,
            distance_km=station.distance_km,
            last_verified_at=station.last_verified_at,
            created_at=station.created_at,
            updated_at=station.updated_at,
        )
        station_responses.append(station_response)
        
        # Track cheapest station (only if price is available)
        if station.gasolina_comum_price is not None and station.gasolina_comum_price < cheapest_price:
            cheapest_price = station.gasolina_comum_price
            cheapest_station_id = str(station.station_id)
    
    return StationListResponse(
        stations=station_responses,
        count=len(station_responses),
        cheapest_station_id=cheapest_station_id,
        search_center={"latitude": latitude, "longitude": longitude},
        search_radius_km=radius_km,
    )


@router.patch("/{station_id}", response_model=StationResponse)
def update_station_price(
    station_id: str,
    update_data: StationUpdate,
    db: Session = Depends(get_db),
):
    """
    Update station price and status (admin override).
    
    **Phase 2.2 Implementation:**
    - Allows manual updates to gasolina_comum_price and status
    - Automatically updates last_verified_at to current timestamp
    - Returns updated station data
    
    Path Parameters:
        - station_id: UUID of the station to update
    
    Request Body:
        - gasolina_comum_price: Optional new price
        - status: Optional new status (Success, No Data, Pending)
    
    Returns:
        Updated StationResponse with new values and timestamp
    
    Raises:
        HTTPException 404: If station not found
    """
    # Convert station_id string to UUID for database lookup
    try:
        station_uuid = UUID(station_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid station_id format (must be UUID)")
    
    # Query the station from database
    station = db.query(Station).filter(Station.station_id == station_uuid).first()
    
    if not station:
        raise HTTPException(status_code=404, detail=f"Station with id {station_id} not found")
    
    # Update fields if provided
    if update_data.gasolina_comum_price is not None:
        station.gasolina_comum_price = update_data.gasolina_comum_price
    
    if update_data.status is not None:
        station.status = update_data.status
    
    # Always update the last_verified_at timestamp on any update
    station.last_verified_at = datetime.now(timezone.utc)
    
    # Commit changes to database
    db.commit()
    db.refresh(station)
    
    # Return updated station
    return StationResponse(
        station_id=str(station.station_id),
        name=station.name,
        phone_number=station.phone_number,
        address=station.address,
        city=station.city,
        latitude=station.latitude,
        longitude=station.longitude,
        bandeira=station.bandeira,
        gasolina_comum_price=station.gasolina_comum_price,
        status=station.status,
        distance_km=None,  # Distance not applicable for single station update
        last_verified_at=station.last_verified_at,
        created_at=station.created_at,
        updated_at=station.updated_at,
    )
