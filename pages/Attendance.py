import customtkinter
import sys
import os
import threading
import time

from datetime import timedelta
from FaceRecognitionModal import FaceRecognitionModal
from DatabaseManager import DatabaseManager

class Attendance(FaceRecognitionModal):
  def __init__(self):
    try:
      super().__init__()

      DatabaseManager.AttendanceRows = []
      self.headers = [
        "Student ID",
        "First Name",
        "Middle Name",
        "Last Name",
        "Attendance Time"
      ]

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  
  def parseTimedelta(self, time):
    hours, minutes = map(int, time.split(':'))
    return timedelta(hours=hours, minutes=minutes)

  def displayAttendanceTable(self):
    try:
      for label in DatabaseManager.AttendanceRows:
        label.destroy()

      if len(DatabaseManager.Attendance) > 0:
        for row, log in enumerate(DatabaseManager.Attendance, start = 1):
          AttendanceTime, StudentID, StudentFirstName, StudentMiddleName, StudentLastName = log

          attendance_data = [
            StudentID,
            StudentFirstName,
            StudentMiddleName,
            StudentLastName,
            AttendanceTime
          ]

          for col, data in enumerate(attendance_data):
              data_label = customtkinter.CTkLabel(
                DatabaseManager.Attendance_table_frame,
                text=data,
                padx=10,
                pady=5
              )
              data_label.grid(row=row, column=col, sticky="nsew")
              DatabaseManager.AttendanceRows.append(data_label)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  
  def refresh(self):
    try:
      while True:
        self.getAttendance()
        self.displayAttendanceTable()
        time.sleep(5)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def create(self, parent):
    try:
      DatabaseManager.Attendance_table_frame = customtkinter.CTkScrollableFrame(parent)
      DatabaseManager.Attendance_table_frame.pack(
        fill="both",
        expand=True
      )

      for col, header in enumerate(self.headers):
        header_label = customtkinter.CTkLabel(
          DatabaseManager.Attendance_table_frame,
          text=header,
          padx=10,
          pady=5
        )
        header_label.grid(
          row=0,
          column=col,
          sticky="nsew"
        )

      for col in range(len(self.headers)):
        DatabaseManager.Attendance_table_frame.columnconfigure(
          col,
          weight=1
        )
      
      threading.Thread(target=self.refresh).start()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)