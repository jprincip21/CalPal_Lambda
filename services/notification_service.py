# SFWRTECH 4SA3 - Software Architecture
# CalPal Project - Notification Service
# Jonathan Principato (400527847)


import os
import resend
from repositories.schedule_repository import ScheduleRepository
from repositories.shift_repository import ShiftRepository
from repositories.employee_repository import EmployeeRepository
from datetime import datetime, timedelta

class NotificationService():
    def __init__(self, 
                 schedule_repo: ScheduleRepository, 
                 shift_repo: ShiftRepository, 
                 employee_repo: EmployeeRepository):
        
        self.__schedule_repo = schedule_repo
        self.__shift_repo = shift_repo
        self.__employee_repo = employee_repo
        self.email_formatter = EmailFormatter()
        self.r = resend.Emails
        resend.api_key = os.environ["RESEND_API_KEY"]

    def send_schedule_notification(self, schedule_id):
        schedule = self.__schedule_repo.get(schedule_id)

        info = schedule.get_schedule_info()
        location_id = info["location_id"]
        location_name = info["location_name"]
        start_date = self.email_formatter._format_date(info["start_date"])
        end_date = self.email_formatter._format_date(info["end_date"])

        shifts = self.__shift_repo.get_shifts_by_schedule_id(schedule_id)
        
        employees = self.__employee_repo.get_employees_by_location_id(location_id)
        
        formatted_email = self.email_formatter._build_email(info, employees, shifts)

        for employee in employees:
            employee_info = employee.get_employee_info()
            employee_email = employee_info["email"]

            self.r.send({
                "from": "CalPal <calpal@jprincip.me>",
                "to": employee_email,
                "subject": f"{location_name} Schedule | {start_date} - {end_date}",
                "html": formatted_email
            })

    
class EmailFormatter:
    def _build_email(self, schedule_info, employees, shifts):

        formatted_start = self._format_date(schedule_info["start_date"])
        formatted_end = self._format_date(schedule_info["end_date"])

        # Generate a list of dates
        start = datetime.strptime(schedule_info["start_date"], "%Y-%m-%d")
        dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]  # ✓
        display_dates = [(start + timedelta(days=i)).strftime("%b %d %Y") for i in range(7)] 
        day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        # Create a lookup for shifts: {employee_id: {date: shift_info}}
        shift_lookup = {}
        for shift in shifts:

            shift_info = shift.get_shift_info()
            employee_id = shift_info["employee_id"]
            shift_date = shift_info["start_datetime"].split(" ")[0]

            if employee_id not in shift_lookup:
                shift_lookup[employee_id] = {}

            shift_lookup[employee_id][shift_date] = shift_info 

        # Table Header
        header_cells = "".join([
            f"""
            <th style="padding: 10px 5px; background-color: #9b87f5; color: #ffffff;
                    font-size: 13px; text-align: center; border: 1px solid #e3e4e6; 
                    white-space: nowrap; width: 90px; line-height: 1.4;">
                <span style="display: block; font-weight: bold;">{day_names[i]}</span>
                <span style="display: block; font-weight: normal; font-size: 10px; color: #ffffff; opacity: 0.9;">
                    {display_dates[i]}
                </span>
            </th>
            """
            for i, date in enumerate(dates)
        ])

        # Table Rows
        rows = ""
        for i, employee in enumerate(employees):
            employee_info = employee.get_employee_info()
            employee_id = employee_info["id"]
            bg_color = "#f8f7ff" if i % 2 == 0 else "#ffffff"

            cells = ""
            for date in dates:
                # Only create cells for employees that have shifts and when were on a certain date
                if employee_id in shift_lookup and date in shift_lookup[employee_id]:
                    
                    # Get Shift Information
                    shift = shift_lookup[employee_id][date]
                    raw_start = shift["start_datetime"].split(" ")[1][:5]
                    raw_end = shift["end_datetime"].split(" ")[1][:5]

                    start_time = datetime.strptime(raw_start, "%H:%M").strftime("%I:%M %p").lstrip("0")
                    end_time = datetime.strptime(raw_end, "%H:%M").strftime("%I:%M %p").lstrip("0")
                    
                    is_overnight = shift["end_datetime"].split(" ")[0] > shift["start_datetime"].split(" ")[0]
                    overnight_indicator = '<span style="color: #9b87f5;">Overnight</span>' if is_overnight else ""

                    cells += f"""
                        <td style="padding: 10px 14px; text-align: center; 
                        border: 1px solid #e3e4e6; font-size: 12px; color: #373f4a;">
                            {overnight_indicator}<br/>{start_time}<br/>{end_time}
                        </td>
                    """
                else:
                    # If no shift exists display "-"
                    cells += f"""
                        <td style="padding: 10px 14px; text-align: center; 
                        border: 1px solid #e3e4e6; font-size: 12px;">
                        -
                        </td>
                    """
            rows += f"""
                <tr style="background-color: {bg_color}; border-bottom: 1px solid #e3e4e6;">
                    <td style="padding: 10px 14px; font-weight: 600; font-size: 13px;
                    border: 1px solid #e3e4e6; white-space: nowrap; color: #373f4a;">
                        {employee_info['first_name']} {employee_info['last_name']}
                    </td>
                        {cells}
                </tr>
            """

        # Build Entire Email
        html = f"""
            <!-- Header -->
            <div style="font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; 
            border: 1px solid #e3e4e6; border-radius: 8px; background-color: #f8f7ff">
                <div style="background-color: #9b87f5; padding: 24px; border-radius: 8px 8px 0 0;
                font-family: Arial, sans-serif">
                    <h1 style="color: white; margin: 0; font-size: 24px;">CalPal</h1>
                    <p style="color: #FAFAFA; margin: 8px 0 0 0; font-size: 14px;">Schedule Notification</p>
                </div>

                <div style="font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 24px">
                    
                    <!-- Body -->
                    <div style="border-top: none; border-bottom: 1px solid #e3e4e6;">
                        <p style="color: #1f1f1f; font-size: 15px;">
                            The schedule for <strong>{schedule_info['location_name']}</strong> has been published
                            for the week of <strong>{formatted_start}</strong> to <strong>{formatted_end}</strong>.
                        </p>
                    </div>

                <!-- Table Head -->
                    <div style="overflow-x: auto; margin-top: 20px">
                        <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;">
                            <thead>
                                <tr>
                                    <th style="padding: 10px 14px; background-color: #9b87f5; color: white;
                                    font-size: 12px; text-align: center; border: 1px solid #e3e4e6;">
                                    Employee
                                    </th>
                                    {header_cells}
                                </tr>
                            </thead>

                            <!-- Table Body -->
                            <tbody>
                                {rows}
                            </tbody>
                        </table>
                    </div>
                    <p style="color: #6b7280; font-size: 13px; margin-top: 24px;">
                        If you have any questions please contact your manager.
                    </p>
                </div>
            </div>
        """

        return html

    def _format_date(self, date):
        #convert date to date object (YYYY-MM-DD)
        date_object = datetime.strptime(date, "%Y-%m-%d")

        # Convert date object into reformatted string (Month Day, Year)
        formatted_date = date_object.strftime("%b %d, %Y")
        return formatted_date

