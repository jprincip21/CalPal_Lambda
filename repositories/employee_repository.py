# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Employee Repository
# Jonathan Principato (400527847)

from repositories.repository import Repository
from models.employee import Employee

# Design Pattern: Repository Pattern
# EmployeeRepository handles all database operations for Employee entities.
# It extends the abstract Repository class and depends on the DBConnection singleton.
# This decouples the database logic from the router layer.

class EmployeeRepository(Repository):
    def __init__(self, db):
        super().__init__(db)

    def get(self, id: int) -> Employee:
        """Retrieve a single employee by ID"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Employees WHERE id = %s", (id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return None
        return Employee(**result)
    
    def get_all(self) -> list[Employee]:
        """Retrieve all employees"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Employees")
        result = cursor.fetchall()
        cursor.close()
        return [Employee(**row) for row in result]

    def create(self, entity: Employee, location_id: int | None = None) -> None:
        """Insert a new employee into the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        info = entity.get_employee_info()
        cursor.execute("""
            INSERT INTO Employees 
            (first_name, last_name, address, city, province_state_region, country, 
            postal_zip_code, phone_number, email, job_title, wage_type, wage, hire_date, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            info['first_name'],
            info['last_name'],
            info['address'],
            info['city'],
            info['province_state_region'],
            info['country'],
            info['postal_zip_code'],
            info['phone_number'],
            info['email'],
            info['job_title'],
            info['wage_type'],
            info['wage'],
            info['hire_date'],
            info['is_active']
        ))

        # Create Employee Location Link
        new_employee_id = cursor.lastrowid
        if location_id is not None:
            cursor.execute("""
                INSERT INTO Employee_Locations (employee_id, location_id) 
                VALUES(%s, %s)
            """, (new_employee_id, location_id))

        conn.commit()
        cursor.close()

    def update(self, entity: Employee, location_id: int | None = None) -> None:
        """Update an existing employee in the database"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        info = entity.get_employee_info()
        cursor.execute("""
            UPDATE Employees SET
            first_name = %s,
            last_name = %s,
            address = %s,
            city = %s,
            province_state_region = %s,
            country = %s,
            postal_zip_code = %s,
            phone_number = %s,
            email = %s,
            job_title = %s,
            wage_type = %s,
            wage = %s,
            hire_date = %s,
            is_active = %s
            WHERE id = %s
        """, (
            info['first_name'],
            info['last_name'],
            info['address'],
            info['city'],
            info['province_state_region'],
            info['country'],
            info['postal_zip_code'],
            info['phone_number'],
            info['email'],
            info['job_title'],
            info['wage_type'],
            info['wage'],
            info['hire_date'],
            info['is_active'],
            info['id']
        ))

        # Update old Employee_Location Link and Create a new one
        if location_id is not None:

            cursor.execute("""
                SELECT employee_id FROM Employee_Locations WHERE employee_id = %s
                """, (info['id'], ))
            existing_link = cursor.fetchone()

            if existing_link:
                cursor.execute("""
                    DELETE FROM Employee_Locations WHERE employee_id = %s
                    """, (info['id'],))
                
            cursor.execute("""
                INSERT INTO Employee_Locations (employee_id, location_id)
                VALUES (%s, %s)
                """, (info['id'], location_id))


        conn.commit()
        cursor.close()

    def delete(self, id: int) -> None:
        """Delete an employee by ID"""
        conn = self.db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employees WHERE id = %s", (id,))
        conn.commit()
        cursor.close()