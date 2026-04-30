"""
Pydantic schemas for request/response validation and API documentation.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.station import StationStatus


class StationBase(BaseModel):
    """Base schema with common station fields."""
    name: str = Field(..., description="Station name")
    phone_number: str = Field(..., description="Station phone number in E.164 format")
    address: str = Field(..., description="Station address")
    city: str = Field(default="São Paulo", description="Station city")
    latitude: float = Field(..., description="Station latitude coordinate")
    longitude: float = Field(..., description="Station longitude coordinate")
    bandeira: str = Field(..., description="Gas station brand/bandeira")
    gasolina_comum_price: Optional[float] = Field(None, description="Current price of common gasoline")
    status: StationStatus = Field(default=StationStatus.PENDING, description="Station data status")


class StationCreate(StationBase):
    """Schema for creating a new station."""
    pass


class StationUpdate(BaseModel):
    """Schema for updating station information (admin override)."""
    gasolina_comum_price: Optional[float] = Field(None, description="Updated gasoline price")
    status: Optional[StationStatus] = Field(None, description="Updated status")


class StationResponse(StationBase):
    """Schema for returning station data with calculated fields."""
    station_id: str = Field(..., description="Unique station identifier (UUID)")
    distance_km: Optional[float] = Field(None, description="Distance from search point in kilometers")
    last_verified_at: Optional[datetime] = Field(None, description="Last verification timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True  # Allow populating from ORM models


class SearchQuery(BaseModel):
    """Schema for spatial search query parameters."""
    latitude: float = Field(..., description="Search center latitude", ge=-90, le=90)
    longitude: float = Field(..., description="Search center longitude", ge=-180, le=180)
    radius_km: float = Field(default=2.0, description="Search radius in kilometers", ge=1.0, le=5.0)


class StationListResponse(BaseModel):
    """Schema for returning a list of stations with metadata."""
    stations: List[StationResponse] = Field(..., description="List of stations")
    count: int = Field(..., description="Total number of stations returned")
    cheapest_station_id: Optional[str] = Field(None, description="ID of the cheapest station in results")
    search_center: dict = Field(..., description="Search center coordinates")
    search_radius_km: float = Field(..., description="Search radius used")
