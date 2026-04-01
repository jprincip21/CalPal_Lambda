# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Shift Router
# Jonathan Principato (400527847)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db_manager
from repositories.shift_repository import ShiftRepository
from models.shift import Shift

router = APIRouter()

# Design Pattern: Repository Pattern
# The router depends on ShiftRepository for all database operations.
# No SQL logic lives in this file, the router only handles HTTP requests and responses.
shift_repo = ShiftRepository(db_manager)

# Pydantic model for request body validation
class ShiftRequest(BaseModel):
    schedule_id: int
    employee_id: int
    date: str
    start_time: str
    end_time: str

@router.get("/schedule/{schedule_id}")
def get_shifts_by_schedule_id(schedule_id: int):
    try:
        shifts = shift_repo.get_shifts_by_schedule_id(schedule_id)
        return [s.get_shift_info() for s in shifts]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.post("")
def create_shift(request: ShiftRequest):
    try:
        shift = Shift(
            id=None,
            schedule_id=request.schedule_id,
            employee_id=request.employee_id,
            date=request.date,
            start_time=request.start_time,
            end_time=request.end_time
        )
        shift_repo.create(shift)
        return {"message": "Shift created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{id}")
def update_shift(id: int, request: ShiftRequest):
    try:
        exisiting = shift_repo.get(id)
        if exisiting is None:
            raise HTTPException(status_code=404, detail="Shift not found")
        shift = Shift(
            id=id,
            schedule_id=request.schedule_id,
            employee_id=request.employee_id,
            date=request.date,
            start_time=request.start_time,
            end_time=request.end_time
        )
        shift_repo.update(shift)
        return {"message": "Shift updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}")
def delete_shift(id: int):
    try:
        existing = shift_repo.get(id)
        if existing is None:
            return HTTPException(status_code=404, detail="Shift not found")
        shift_repo.delete(id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))