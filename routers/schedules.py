# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Schedule Router
# Jonathan Principato (400527847)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db_manager
from repositories.schedule_repository import ScheduleRepository
from models.schedule import Schedule


router = APIRouter()

# Design Pattern: Repository Pattern
# The router depends on ScheduleRepository for all database operations.
# No SQL logic lives in this file, the router only handles HTTP requests and responses.
schedule_repo = ScheduleRepository(db_manager)

# Pydantic model for request body validation
class ScheduleRequest(BaseModel):
    location_id: int
    start_date: str
    end_date: str

@router.get("")
def get_all_schedules():
    try:
        schedules = schedule_repo.get_all()
        return[s.get_schedule_info() for s in schedules]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_schedule(id: int):
    try: 
        schedule = schedule_repo.get(id)
        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return schedule.get_schedule_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("")
def create_schedule(request: ScheduleRequest):
    try:
        schedule = Schedule(
            id=None,
            location_id=request.location_id,
            start_date=request.start_date,
            end_date=request.end_date,
            state='draft'
        )
        schedule_repo.create(schedule)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("")
def delete_schedule(id: int):
    try:
        schedule_repo.delete(id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))