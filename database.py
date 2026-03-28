# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Database Connection
# Jonathan Principato (400527847)

import os
import mysql.connector
from mysql.connector import Error

# Singleton Database connection
# Creational Pattern
# Used to ensure only one db connection is created on each lambda.
# If a lambda is "Warm" it will cut down some time on returning api calls.

class DBConnection():
    __instance = None
    __connection = None

    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(DBConnection, cls).__new__(cls)
        return cls.__instance
    
    def get_db_connection(self):
        if self.__connection is None or not self.__connection.is_connected():
            try:
                self.__connection = mysql.connector.connect(
                                    host=os.environ['DB_HOST'],
                                    user=os.environ['DB_USER'],
                                    password=os.environ['DB_PASS'],
                                    database=os.environ['DB_NAME']
                                )
            except Error as e:
                print(f"Error while connecting to MySQL: {e}")
                raise e
        return self.__connection
db_manager = DBConnection()