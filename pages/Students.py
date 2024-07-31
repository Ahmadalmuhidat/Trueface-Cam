import sys
import os
import customtkinter

from DatabaseManager import DatabaseManager
from CTkMessagebox import CTkMessagebox

class Students(DatabaseManager):
  def __init__(self):
    try:
      super().__init__()

      self.StudentsRows = []
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

  def DisplayStudentsTable(self):
    try:
      for label in self.StudentsRows:
        label.destroy()

      if len(self.ClassStudents) > 0:
        for row, Student in enumerate(self.ClassStudents, start = 1):
          StudentID, \
          StudentFirstName, \
          StudentMiddleName, \
          StudentLastName, \
          StudentGender = Student

          Student_data = [
            StudentID,
            StudentFirstName,
            StudentMiddleName,
            StudentLastName,
            StudentGender
          ]

          for col, data in enumerate(Student_data):
              DataLabel = customtkinter.CTkLabel(
                self.StudentsTableFrame,
                text = data,
                padx = 10,
                pady = 5
              )
              DataLabel.grid(
                row = row,
                column = col,
                sticky = "nsew"
              )
              self.StudentsRows.append(DataLabel)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
  
  def Refresh(self):
    try:
      if not DatabaseManager.CurrentClass:
          title = "Error"
          message = "Please select a lecture from the settings"
          icon = "cancel"
          CTkMessagebox(title=title, message=message, icon=icon)
          return

      self.GetClassStudents()
      self.DisplayStudentsTable()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

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

      self.StudentsTableFrame = customtkinter.CTkScrollableFrame(parent)
      self.StudentsTableFrame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(self.headers):
        HeaderLabel = customtkinter.CTkLabel(
          self.StudentsTableFrame,
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
        self.StudentsTableFrame.columnconfigure(
          col,
          weight = 1
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)