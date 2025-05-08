import sys
import os
import customtkinter
import pandas

from CTkMessagebox import CTkMessagebox
from app.core.data_manager import Data_Manager
from app.controllers.attendance import get_current_class_attendance, search_attendance
from app.controllers.reports import get_report

class Attendance():
  def __init__(self):
    self._data_manager = Data_Manager()

    self._attendance = []
    self._headers = [
      "Student ID",
      "First Name",
      "Middle Name",
      "Last Name",
      "Attendance Time"
    ]

  def generate_report(self):
    try:
      get_report(
        self._data_manager.get_start_time(),
        self._data_manager.get_allowed_minutes()
      )

      report = pandas.DataFrame(
        self._data_manager.get_current_lecture_attendance_report(),
        columns = [
          "Student ID",
          "First Name",
          "Middle Name",
          "Last Name",
          "Attendance Time",
          "Lateness"
        ]
      )

      downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
      file_name = "Attendance Report.xlsx"
      file_path = os.path.join(downloads_folder, file_name)
      report.to_excel(
        file_path,
        index = False
      )

      title = "Generate complete"
      message = "you can find the report in {}".format(downloads_folder)
      icon = "check"
      CTkMessagebox(
        title = title,
        message = message,
        icon = icon
      )

      self._data_manager.get_current_lecture_attendance_report().clear()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def display_attendance_table(self):
    try:
      for label in self._attendance:
        label.destroy()

      if len(self._data_manager.get_current_lecture_attendance()) > 0:
        for row, attendance in enumerate(self._data_manager.get_current_lecture_attendance(), start = 1):
          attendance_row = [
            attendance.get_student().get_student_id(),
            attendance.get_student().get_first_name(),
            attendance.get_student().get_middle_name(),
            attendance.get_student().get_last_name(),
            attendance.get_time()
          ]

          for col, data in enumerate(attendance_row):
            attendance_data = customtkinter.CTkLabel(
              self.attendance_table_frame,
              text = data,
              padx = 10,
              pady = 5   
            )
            attendance_data.grid(
              row = row,
              column = col,
              sticky = "nsew"
            )
            self._attendance.append(attendance_data)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
  
  def refresh(self):
    try:
      if not self._data_manager.get_current_class():
        title = "Error"
        message = "Please select a lecture from the settings"
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message,
          icon = icon
        )
        return

      get_current_class_attendance()
      self.display_attendance_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def search(self, term):
    try:
      search_attendance(term)
      self.display_attendance_table()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def lunch_view(self, parent):
    try:
      search_bar_frame = customtkinter.CTkFrame(
        parent,
        bg_color = "transparent"
      )
      search_bar_frame.pack(
        fill = "x",
        expand = False
      )

      search_button = customtkinter.CTkButton(
        search_bar_frame,
        command = lambda: self.search(search_bar.get()),
        text = "Search"
      )
      search_button.grid(
        row = 0,
        column = 0,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )

      search_bar = customtkinter.CTkEntry(
        search_bar_frame,
        width = 400,
        placeholder_text = "Search for Students..."
      )
      search_bar.grid(
        row = 0,
        column = 1,
        sticky = "nsew",
        pady = 10
      )

      refresh_button = customtkinter.CTkButton(
        search_bar_frame,
        command = self.refresh,
        width = 100,
        text = "Refresh"
      )
      refresh_button.grid(
        row = 0,
        column = 2,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )

      report_button = customtkinter.CTkButton(
        search_bar_frame,
        command = self.generate_report,
        width = 100,
        text = "Generate Report"
      )
      report_button.grid(
        row = 0,
        column = 3,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )

      self.attendance_table_frame = customtkinter.CTkScrollableFrame(parent)
      self.attendance_table_frame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(self._headers):
        header_label = customtkinter.CTkLabel(
          self.attendance_table_frame,
          text = header,
          padx = 10,
          pady = 5   
        )
        header_label.grid(
          row = 0,
          column = col,
          sticky = "nsew"
        )

      for col in range(len(self._headers)):
        self.attendance_table_frame.columnconfigure(
          col,
          weight = 1
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)