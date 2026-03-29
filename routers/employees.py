# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Employee Router
# Jonathan Principato (400527847)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import db_manager
from repositories.employee_repository import EmployeeRepository
from models.employee import Employee
from datetime import date, datetime

router = APIRouter()

# Design Pattern: Repository Pattern
# The router depends on EmployeeRepository for all database operations.
# No SQL logic lives in this file, the router only handles HTTP requests and responses.
employee_repo = EmployeeRepository(db_manager)

# Pydantic model for request body validation
class EmployeeRequest(BaseModel):
    first_name: str
    last_name: str
    address: str
    city: str
    province_state_region: str
    country: str
    postal_zip_code: str
    phone_number: str
    email: str
    job_title: str
    wage_type: str
    wage: float
    hire_date: str
    is_active: bool

@router.get("")
def get_all_employees():
    try:
        employees = employee_repo.get_all()
        return [e.get_employee_info() for e in employees]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}")
def get_employee(id: int):
    try:
        employee = employee_repo.get(id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee.get_employee_info()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("")
def create_employee(request: EmployeeRequest):
    valid_date = request.hire_date
    try:
        datetime.strptime(valid_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        valid_date = datetime.now().strftime("%Y-%m-%d")
    try:
        employee = Employee(
            id=None,
            first_name=request.first_name,
            last_name=request.last_name,
            address=request.address,
            city=request.city,
            province_state_region=request.province_state_region,
            country=request.country,
            postal_zip_code=request.postal_zip_code,
            phone_number=request.phone_number,
            email=request.email,
            job_title=request.job_title,
            wage_type=request.wage_type,
            wage=request.wage,
            hire_date=valid_date,
            is_active=request.is_active
        )
        employee_repo.create(employee)
        return {"message": "Employee created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}")
def update_employee(id: int, request: EmployeeRequest):
    
    try:
        existing = employee_repo.get(id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        valid_date = request.hire_date
        try:
            datetime.strptime(valid_date, "%Y-%m-%d")
        except (ValueError, TypeError):
            valid_date = datetime.now().strftime("%Y-%m-%d")

        employee = Employee(
            id=id,
            first_name=request.first_name,
            last_name=request.last_name,
            address=request.address,
            city=request.city,
            province_state_region=request.province_state_region,
            country=request.country,
            postal_zip_code=request.postal_zip_code,
            phone_number=request.phone_number,
            email=request.email,
            job_title=request.job_title,
            wage_type=request.wage_type,
            wage=request.wage,
            hire_date=valid_date,
            is_active=request.is_active
        )
        employee_repo.update(employee)
        return {"message": "Employee updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
def delete_employee(id: int):
    try:
        existing = employee_repo.get(id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        employee_repo.delete(id)
        return {"message": "Employee deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))