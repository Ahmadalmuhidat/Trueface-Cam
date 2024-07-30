import sys
import os
import customtkinter
import pandas

from FaceRecognitionModal import FaceRecognitionModal
from CTkMessagebox import CTkMessagebox
from DatabaseManager import DatabaseManager

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

  def GenerateReport(self):
    try:
      self.GetReport(
        DatabaseManager.StartTime,
        DatabaseManager.AllowedMinutes
      )

      report = pandas.DataFrame(
        DatabaseManager.Report,
        columns = [
          "Student ID",
          "First Name",
          "Middle Name",
          "Last Name",
          "Attendance Time",
          "Lateness"
        ]
      )

      DownloadsFolder = os.path.join(os.path.expanduser("~"), "Downloads")
      FileName = "Attendance Report.xlsx"
      FilePath = os.path.join(DownloadsFolder, FileName)
      report.to_excel(
        FilePath,
        index = False
      )

      title = "Generate complete"
      message = "you can find the report in {}".format(DownloadsFolder)
      icon = "check"
      CTkMessagebox(
        title = title,
        message = message,
        icon = icon
      )

      DatabaseManager.Report.clear()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def DisplayAttendanceTable(self):
    try:
      for label in self.AttendanceRows:
        label.destroy()

      if len(self.Attendance) > 0:
        for row, Attendance in enumerate(self.Attendance, start = 1):
          StudentID, \
          StudentFirstName, \
          StudentMiddleName, \
          StudentLastName, \
          AttendanceTime = Attendance

          attendance_data = [
            StudentID,
            StudentFirstName,
            StudentMiddleName,
            StudentLastName,
            AttendanceTime
          ]

          for col, data in enumerate(attendance_data):
            DataLabel = customtkinter.CTkLabel(
              self.AttendanceTableFrame,
              text = data,
              padx = 10,
              pady = 5   
            )
            DataLabel.grid(
              row = row,
              column = col,
              sticky = "nsew"
            )
            self.AttendanceRows.append(DataLabel)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  
  def Refresh(self):
    try:
      if not DatabaseManager.CurrentClass:
        title = "Error"
        message = "Please select a lecture from the settings"
        icon = "cancel"
        CTkMessagebox(
          title=title,
          message=message,
          icon=icon
        )
        return

      self.GetCurrentClassAttendance()
      self.DisplayAttendanceTable()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Search(self, term):
    try:
      self.SearchAttendance(term)
      self.DisplayAttendanceTable()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Create(self, parent):
    try:
      SearchBarFrame = customtkinter.CTkFrame(
        parent,
        bg_color = "transparent"
      )
      SearchBarFrame.pack(
        fill = "x",
        expand = False
      )

      SearchButton = customtkinter.CTkButton(
        SearchBarFrame,
        command = lambda: self.Search(SearchBar.get()),
        text = "Search"
      )
      SearchButton.grid(
        row = 0,
        column = 0,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )

      SearchBar = customtkinter.CTkEntry(
        SearchBarFrame,
        width = 400,
        placeholder_text = "Search for Students..."
      )
      SearchBar.grid(
        row = 0,
        column = 1,
        sticky = "nsew",
        pady = 10
      )

      RefreshButton = customtkinter.CTkButton(
        SearchBarFrame,
        command = self.Refresh,
        width = 100,
        text = "Refresh"
      )
      RefreshButton.grid(
        row = 0,
        column = 2,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )

      ReportButton = customtkinter.CTkButton(
        SearchBarFrame,
        command = self.GenerateReport,
        width = 100,
        text = "Generate Report"
      )
      ReportButton.grid(
        row = 0,
        column = 3,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )

      self.AttendanceTableFrame = customtkinter.CTkScrollableFrame(parent)
      self.AttendanceTableFrame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(self.headers):
        HeaderLabel = customtkinter.CTkLabel(
          self.AttendanceTableFrame,
          text = header,
          padx = 10,
          pady = 5   
        )
        HeaderLabel.grid(
          row = 0,
          column = col,
          sticky = "nsew"
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