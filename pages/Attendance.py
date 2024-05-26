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
                self.Attendance_table_frame,
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
      self.getAttendance()
      self.displayAttendanceTable()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def search(self, term):
    try:
      self.searchAttendance(term)
      self.displayAttendanceTable()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def create(self, parent):
    try:
      search_bar_frame = customtkinter.CTkFrame(parent, bg_color="transparent")
      search_bar_frame.pack(fill="x", expand=False)

      search_button = customtkinter.CTkButton(search_bar_frame, text="Search")
      search_button.grid(row=0, column=0, sticky="nsew", pady=10, padx=5)
      search_button.configure(command=lambda: self.search(search_bar.get()))

      search_bar = customtkinter.CTkEntry(search_bar_frame)
      search_bar.grid(row=0, column=1, sticky="nsew", pady=10)
      search_bar.configure(width=400, placeholder_text="Search for Students...")

      reset_button = customtkinter.CTkButton(search_bar_frame, width=100, text="Refresh")
      reset_button.grid(row=0, column=2, sticky="nsew", pady=10, padx=5)
      reset_button.configure(command=self.refresh)

      self.Attendance_table_frame = customtkinter.CTkScrollableFrame(parent)
      self.Attendance_table_frame.pack(
        fill="both",
        expand=True
      )

      for col, header in enumerate(self.headers):
        header_label = customtkinter.CTkLabel(
          self.Attendance_table_frame,
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
        self.Attendance_table_frame.columnconfigure(
          col,
          weight=1
        )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)