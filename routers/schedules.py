# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Schedule Router
# Jonathan Principato (400527847)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db_manager
from repositories.schedule_repository import ScheduleRepository
from models.schedule import Schedule
from states.get_state import get_state
from repositories.shift_repository import ShiftRepository
from repositories.employee_repository import EmployeeRepository
from services.notification_service import NotificationService

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

class StateRequest(BaseModel):
    action: str

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
    except HTTPException:
        raise
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
        return {"message": "Schedule created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}")
def delete_schedule(id: int):
    try:
        existing = schedule_repo.get(id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        schedule_repo.delete(id)
        return {"message": "Schedule Deleted Successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/{id}/state")
def update_schedule_state(id: int, request: StateRequest):

    shift_repo = ShiftRepository(db_manager)
    employee_repo = EmployeeRepository(db_manager)
    notification_service = NotificationService(schedule_repo, shift_repo, employee_repo)

    try:
        existing = schedule_repo.get(id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        
        if request.action not in ["publish", "complete"]:
            raise HTTPException(status_code=400, detail="Action must be publish or complete")

        info = existing.get_schedule_info()
        state = get_state(info["state"], id, schedule_repo, shift_repo)

        if request.action == "publish":
            state.publish(notification_service)
        elif request.action == "complete":
            state.complete()

        return {"message": f"Schedule state updated to {request.action} successfully"}   
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))