from fastapi import APIRouter, HTTPException
from database import db_manager

router = APIRouter()

@router.get("")
def get_all_employees():
    try:
        conn = db_manager.get_db_connection()
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