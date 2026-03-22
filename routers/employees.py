from fastapi import APIRouter, HTTPException
from database import get_db_connection

router = APIRouter(
    prefix="/employees",  # All routes in this file start with /employees
    tags=["Employees"]    # Groups Endpoints in the SwaggerUI auto-generated docs
)

@router.get("/")
def get_all_employees():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Employees")
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()