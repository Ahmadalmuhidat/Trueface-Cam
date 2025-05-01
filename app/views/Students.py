import sys
import os
import customtkinter

from app.core.data_manager import DataManager
from app.controllers.students import get_classes_students
from CTkMessagebox import CTkMessagebox

class Students():
  def __init__(self):
    try:
      super().__init__()

      self.data_manager = DataManager()

      self.students = []
      self.headers = [
        "Student ID",
        "First Name",
        "Middle Name",
        "Last Name",
        "Gender"
      ]

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def display_students_table(self):
    try:
      for label in self.students:
        label.destroy()

      if len(self.data_manager.current_class_students) > 0:
        for row, student in enumerate(self.current_class_students, start = 1):
          student_row = [
            student.id,
            student.first_name,
            student.middle_name,
            student.last_name,
            student.gender
          ]

          for col, data in enumerate(student_row):
              student_data = customtkinter.CTkLabel(
                self.students_table_frame,
                text = data,
                padx = 10,
                pady = 5
              )
              student_data.grid(
                row = row,
                column = col,
                sticky = "nsew"
              )
              self.students.append(student_data)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
  
  def refresh(self):
    try:
      if not self.data_manager.current_class:
          title = "Error"
          message = "Please select a lecture from the settings"
          icon = "cancel"
          CTkMessagebox(
            title=title,
            message=message,
            icon=icon
          )
          return

      get_classes_students()
      self.display_students_table()

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

      self.students_table_frame = customtkinter.CTkScrollableFrame(parent)
      self.students_table_frame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(self.headers):
        header_label = customtkinter.CTkLabel(
          self.students_table_frame,
          text = header,
          padx = 10,
          pady = 5
        )
        header_label.grid(
          row = 0,
          column = col,
          sticky = "nsew"
        )

      for col in range(len(self.headers)):
        self.students_table_frame.columnconfigure(
          col,
          weight = 1
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)