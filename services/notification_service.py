# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Notification Service
# Jonathan Principato (400527847)


import os
import resend
from repositories.schedule_repository import ScheduleRepository
from repositories.shift_repository import ShiftRepository
from repositories.employee_repository import EmployeeRepository

class NotificationService():
    def __init__(self, 
                 schedule_repo: ScheduleRepository, 
                 shift_repo: ShiftRepository, 
                 employee_repo: EmployeeRepository):
        
        self.__schedule_repo = schedule_repo
        self.__shift_repo = shift_repo
        self.__employee_repo = employee_repo
        self.r = resend.Emails
        resend.api_key = os.environ['RESEND_API_KEY']

    def send_schedule_notification(self, schedule_id):
        schedule = self.__schedule_repo.get(schedule_id)

        info = schedule.get_schedule_info()
        location_id = info["location_id"]
        location_name = info["location_name"]
        start_date = info["start_date"]
        end_date = info["end_date"]

        shifts = self.__shift_repo.get_shifts_by_schedule_id(schedule_id)
        
        employees = self.__employee_repo.get_employees_by_location_id(location_id)

        for employee in employees:
            employee_info = employee.get_employee_info()
            employee_email = employee_info["email"]

            self.r.send({
                "from": "CalPal <calpal@jprincip.me>",
                "to": employee_email,
                "subject": f"{location_name} Schedule | {start_date} - {end_date}",
                "html": "<p>Schedule</p>"
            })
