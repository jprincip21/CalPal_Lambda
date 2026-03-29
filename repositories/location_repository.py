# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Location Repository
# Jonathan Principato (400527847)

from repositories.repository import Repository
from models.location import Location

# Design Pattern: Repository Pattern
# LocationRepository handles all database operations for Location entities.
# It extends the abstract Repository class and depends on the DBConnection singleton.
# This decouples the database logic from the router layer.

class LocationRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def get(self, id: int) -> Location:
        """Retrive a location by id"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Work_Locations WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        return Location(**result)


    def get_all(self) -> list[Location]:
        """Retrieve all locations"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Work_Locations")
        result = cursor.fetchall()
        cursor.close()
        return [Location(**row) for row in result]
    
    def create(self, entity: Location) -> None:
        """Insert a new location into the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        info = entity.get_location_info()
        cursor.execute("""
            INSERT INTO Work_Locations
            (name, address, city, province_state_region, 
            country, postal_zip_code, location_phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            info['name'],
            info['address'],
            info['city'],
            info['province_state_region'],
            info['country'],
            info['postal_zip_code'],
            info['location_phone']
        ))
        conn.commit()
        cursor.close()

    def update(self, entity: Location) -> None:
        """Update an existing location in the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        info = entity.get_location_info()
        cursor.execute(""" UPDATE Work_Locations SET
            name = %s,
            address = %s,
            city = %s,
            province_state_region = %s,
            country = %s,
            postal_zip_code = %s,
            location_phone = %s
            WHERE id = %s
        """, (
            info['name'],
            info['address'],
            info['city'],
            info['province_state_region'],
            info['country'],
            info['postal_zip_code'],
            info['location_phone'],
            info['id']
        ))
        conn.commit()
        cursor.close()

    def delete(self, id: int) -> None:
        """Delete a location by ID"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Work_Locations WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        
