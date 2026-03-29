# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Location Model
# Jonathan Principato (400527847)

# Represents a Location entity in the CalPal system.
# Maps to the Work Locations table in the CalPal MySQL database.
# Used by LocationRepository to structure data returned from the database.

class Location:
    def __init__(self,
                 id,
                 name,
                 address,
                 city,
                 province_state_region,
                 country,
                 postal_zip_code,
                 location_phone
                 ):
        self.__id = id
        self.__name = name
        self.__address = address
        self.__city = city
        self.__province_state_region = province_state_region
        self.__country = country
        self.__postal_zip_code = postal_zip_code
        self.__location_phone = location_phone

    def get_location_info(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "address": self.__address,
            "city": self.__city,
            "province_state_region": self.__province_state_region,
            "country": self.__country,
            "postal_zip_code": self.__postal_zip_code,
            "location_phone": self.__location_phone,
        }