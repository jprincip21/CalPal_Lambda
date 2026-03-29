# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Employee Router
# Jonathan Principato (400527847)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db_manager
from repositories.location_repository import LocationRepository
from models.location import Location

router = APIRouter()
# Design Pattern: Repository Pattern
# The router depends on LocationRepository for all database operations.
# No SQL logic lives in this file, the router only handles HTTP requests and responses.

location_repo = LocationRepository(db_manager)

# Pydantic model for request body validation
class LocationRequest(BaseModel):
    name: str
    address: str
    city: str
    province_state_region: str
    country: str
    postal_zip_code: str
    location_phone: str

@router.get("")
def get_all_locations():
    try:
        locations = location_repo.get_all()
        return [l.get_location_info() for l in locations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("")
def create_location(request: LocationRequest):
    try:
        location = Location(
            id=None,
            name=request.name,
            address=request.address,
            city=request.city,
            province_state_region=request.province_state_region,
            country=request.country,
            postal_zip_code=request.postal_zip_code,
            location_phone=request.location_phone
        )
        location_repo.create(location)
        return {"message": "Location created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{id}")
def update_location(id: int, request: LocationRequest):
    try:
        existing = location_repo.get(id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Location not found")
        location = Location(
            id=id,
            name=request.name,
            address=request.address,
            city=request.city,
            province_state_region=request.province_state_region,
            country=request.country,
            postal_zip_code=request.postal_zip_code,
            location_phone=request.location_phone
        )
        location_repo.update(location)
        return {"message": "Location updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}")
def delete_location(id: int):
    try: 
        existing = location_repo.get(id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Location Not Found")
        location_repo.delete(id)
        return {"message": "Location deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))