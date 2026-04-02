# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Shift Repository
# Jonathan Principato (400527847)

from repositories.repository import Repository
from models.shift import Shift

# Design Pattern: Repository Pattern
# ShiftRepository handles all database operations for Shift entities.
# It extends the abstract Repository class and depends on the DBConnection singleton.
# This decouples the database logic from the router layer.

class ShiftRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    # DELETE IF UNUSED
    def get(self, id: int) -> Shift:
        """Retreive a single shift by id"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Shifts WHERE id = %s", (id, ))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        return Shift(**result)
    
    # SET to pass if unused
    # WE WILL PROBABLY ONLY BE USING GET BY SCHEDULE ID
    def get_all(self) -> list[Shift]:
        """Retreive all shifts"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Shifts")
        rows = cursor.fetchall()
        cursor.close()
        return [Shift(**row) for row in rows]
    
    def get_shifts_by_schedule_id(self, schedule_id: int) -> list[Shift]:
        """Retreive all shifts assigned to a specific schedule"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Shifts WHERE schedule_id = %s", (schedule_id,))
        rows = cursor.fetchall()
        cursor.close()
        return [Shift(**row) for row in rows]
    
    def create(self, entity: Shift) -> None:
        """Create a new shift in the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        info = entity.get_shift_info()
        cursor.execute("""
            INSERT INTO Shifts
            (schedule_id, employee_id, start_datetime, end_datetime)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            info['schedule_id'],
            info['employee_id'],
            info['start_datetime'],
            info['end_datetime']
        ))
        conn.commit()
        cursor.close()
    
    def update(self, entity: Shift) -> None:
        """Update a shift by id"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        info = entity.get_shift_info()
        cursor.execute("""
            UPDATE Shifts SET
            schedule_id = %s,
            employee_id = %s,
            start_datetime = %s,
            end_datetime = %s
            WHERE id = %s
            """, (
                info['schedule_id'],
                info['employee_id'],
                info['date'],
                info['start_datetime'],
                info['end_datetime'],
                info['id']
            ))
        conn.commit()
        cursor.close()

    def delete(self, id: int) -> None:
        """Delete a shift by id"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Shifts WHERE id = %s", (id,))
        conn.commit()
        cursor.close()