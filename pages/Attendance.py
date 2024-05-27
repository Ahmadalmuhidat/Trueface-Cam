import customtkinter
import sys
import os

from datetime import timedelta
from FaceRecognitionModal import FaceRecognitionModal

class Attendance(FaceRecognitionModal):
  def __init__(self):
    try:
      super().__init__()

      self.AttendanceRows = []
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
    return timedelta(
      hours = hours,
      minutes = minutes
    )

  def displayAttendanceTable(self):
    try:
      for label in self.AttendanceRows:
        label.destroy()

      if len(self.Attendance) > 0:
        for row, Attendance in enumerate(self.Attendance, start = 1):
          AttendanceTime, StudentID, StudentFirstName, StudentMiddleName, StudentLastName = Attendance

          attendance_data = [
            StudentID,
            StudentFirstName,
            StudentMiddleName,
            StudentLastName,
            AttendanceTime
          ]

          for col, data in enumerate(attendance_data):
              DataLabel = customtkinter.CTkLabel(self.AttendanceTableFrame)
              DataLabel.grid(
                row = row,
                column = col,
                sticky = "nsew"
              )
              DataLabel.configure(
                text = data,
                padx = 10,
                pady = 5   
              )
              self.AttendanceRows.append(DataLabel)

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
      SearchBarFrame = customtkinter.CTkFrame(parent)
      SearchBarFrame.pack(
        fill = "x",
        expand = False
      )
      SearchBarFrame.configure(bg_color = "transparent")

      SearchButton = customtkinter.CTkButton(SearchBarFrame)
      SearchButton.grid(
        row = 0,
        column = 0,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )
      SearchButton.configure(
        command = lambda: self.search(SearchBar.get()),
        text = "Search"
      )

      SearchBar = customtkinter.CTkEntry(SearchBarFrame)
      SearchBar.grid(
        row = 0,
        column = 1,
        sticky = "nsew",
        pady = 10
      )
      SearchBar.configure(
        width = 400,
        placeholder_text = "Search for Students..."
      )

      RefreshButton = customtkinter.CTkButton(SearchBarFrame)
      RefreshButton.grid(
        row = 0,
        column = 2,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )
      RefreshButton.configure(
        command = self.refresh,
        width = 100,
        text = "Refresh"
      )

      self.AttendanceTableFrame = customtkinter.CTkScrollableFrame(parent)
      self.AttendanceTableFrame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(self.headers):
        HeaderLabel = customtkinter.CTkLabel(self.AttendanceTableFrame)
        HeaderLabel.grid(
          row = 0,
          column = col,
          sticky = "nsew"
        )
        HeaderLabel.configure(
          text = header,
          padx = 10,
          pady = 5   
        )

      for col in range(len(self.headers)):
        self.AttendanceTableFrame.columnconfigure(
          col,
          weight = 1
        )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)