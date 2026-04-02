# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Shift Model
# Jonathan Principato (400527847)

# Represents an Shift entity in the CalPal system.
# Maps to the Shift table in the CalPal MySQL database.
# Used by ShiftRepository to structure data returned from the database.

class Shift:
    def __init__(self,
                 id,
                 schedule_id,
                 employee_id,
                 start_datetime,
                 end_datetime):
        self.__id = id
        self.__schedule_id = schedule_id
        self.__employee_id = employee_id
        self.__start_datetime = start_datetime
        self.__end_datetime = end_datetime

    def get_shift_info(self):
        return {
            "id": self.__id,
            "schedule_id": self.__schedule_id,
            "employee_id": self.__employee_id,
            "start_datetime": str(self.__start_datetime), # Strings instead of date/time objects
            "end_datetime": str(self.__end_datetime)
        }