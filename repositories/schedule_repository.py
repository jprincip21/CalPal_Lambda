# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Schedule Repository
# Jonathan Principato (400527847)

from repositories.repository import Repository
from models.schedule import Schedule

# Design Pattern: Repository Pattern
# ScheduleRepository handles all database operations for Schedule entities.
# It extends the abstract Repository class and depends on the DBConnection singleton.
# This decouples the database logic from the router layer.

class ScheduleRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def get(self, id: int) -> Schedule:
        """Retrieve a single schedule by id"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Schedules WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        return Schedule(**result)
    
    def get_all(self) -> list[Schedule]:
        """Retrieve all schedules"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * from Schedules")
        result = cursor.fetchall()
        cursor.close()
        return [Schedule(**row) for row in result]
    
    def create(self, entity: Schedule) -> None:
        """Create a new schedule in the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        info = entity.get_schedule_info()
        cursor.execute("""
            INSERT INTO Schedules
            (location_id, start_date, end_date, state)
            VALUES (%s, %s, %s, %s)
        """, (
            info['location_id'],
            info['start_date'],
            info['end_date'],
            info['state']
        ))
        conn.commit()
        cursor.close()

    # NO COMPLETE UPDATE FUNCTION FOR SCHEDULES. 
    # If a schedules info is updated all the shifts go along with it 
    # Whether that be the start/end date updated or the location.
    # So it only makes sense to delete the schedule and make a new one
    def update(self, entity: Schedule):
        """NOT IMPLEMENTED: Shedules cannot be updated"""

    def update_state(self, id: int, state: str) -> None:
        """Update an existing schedules information"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Schedules SET state = %s WHERE id = %s
            """, (state, id))
        conn.commit()
        cursor.close()

    def delete(self, id: int) -> None:
        """Delete a schedule from the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Schedules WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
