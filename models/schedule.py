# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Schedule Model
# Jonathan Principato (400527847)

# Represents an Schedule entity in the CalPal system.
# Maps to the Schedule table in the CalPal MySQL database.
# Used by ScheduleRepository to structure data returned from the database.

class Schedule:
    def __init__(self,
                 id,
                 location_id,
                 start_date,
                 end_date,
                 state,
                 location_name=None):
        self.__id = id
        self.__location_id = location_id
        self.__start_date = start_date
        self.__end_date = end_date
        self.__state = state
        self.__location_name = location_name


    def get_schedule_info(self):
        return {
            "id": self.__id,
            "location_id": self.__location_id,
            "start_date": str(self.__start_date), # Strings instead of date objects
            "end_date": str(self.__end_date),
            "state": self.__state,
            "location_name": self.__location_name
        }