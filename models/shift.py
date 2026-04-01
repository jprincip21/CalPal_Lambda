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
                 date,
                 start_time,
                 end_time):
        self.__id = id
        self.__schedule_id = schedule_id
        self.__employee_id = employee_id
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time

    def get_shift_info(self):
        return {
            "id": self.__id,
            "schedule_id": self.__schedule_id,
            "employee_id": self.__employee_id,
            "date": str(self.__date), # Strings instead of date/time objects
            "start_time": str(self.__start_time),
            "end_time": str(self.__end_time)
        }