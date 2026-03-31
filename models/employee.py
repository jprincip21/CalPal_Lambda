# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Employee Model
# Jonathan Principato (400527847)

# Represents an Employee entity in the CalPal system.
# Maps to the Employees table in the CalPal MySQL database.
# Used by EmployeeRepository to structure data returned from the database.

class Employee:
    def __init__(self, 
                 id, 
                 first_name, 
                 last_name, 
                 address, 
                 city,
                 province_state_region, 
                 country, 
                 postal_zip_code,
                 phone_number,
                 email,
                 job_title, 
                 wage_type,
                 wage,
                 hire_date,
                 is_active):
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__address = address
        self.__city = city
        self.__province_state_region = province_state_region
        self.__country = country
        self.__postal_zip_code = postal_zip_code
        self.__phone_number = phone_number
        self.__email = email
        self.__job_title = job_title
        self.__wage_type = wage_type
        self.__wage = wage
        self.__hire_date = hire_date
        self.__is_active = is_active

    def get_employee_info(self):
        return {
            "id": self.__id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "address": self.__address,
            "city": self.__city,
            "province_state_region": self.__province_state_region,
            "country": self.__country,
            "postal_zip_code": self.__postal_zip_code,
            "phone_number": self.__phone_number,
            "email": self.__email,
            "job_title": self.__job_title,
            "wage_type": self.__wage_type,
            "wage": self.__wage,
            "hire_date": self.__hire_date,
            "is_active": self.__is_active
        }