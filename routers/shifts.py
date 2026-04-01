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
schedule_repo = ShiftRepository(db_manager)

# Pydantic model for request body validation
class ShiftRequest(BaseModel):
    schedule_id: int
    employee_id: int
    date: str
    start_time: str
    end_time: str