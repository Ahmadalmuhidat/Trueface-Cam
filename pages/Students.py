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
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

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
              DataLabel = customtkinter.CTkLabel(self.StudentsTableFrame)
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
              self.StudentsRows.append(DataLabel)

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
          CTkMessagebox(title=title, message=message, icon=icon)
          return

      self.GetClassStudents()
      self.DisplayStudentsTable()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Create(self, parent):
    try:
      SearchBarFrame = customtkinter.CTkFrame(parent)
      SearchBarFrame.pack(
        fill = "x",
        expand = False
      )
      SearchBarFrame.configure(bg_color = "transparent")

      RefreshButton = customtkinter.CTkButton(SearchBarFrame)
      RefreshButton.grid(
        row = 0,
        column = 2,
        sticky = "nsew",
        pady = 10,
        padx = 5
      )
      RefreshButton.configure(
        command = self.Refresh,
        width = 100,
        text = "Refresh"
      )

      self.StudentsTableFrame = customtkinter.CTkScrollableFrame(parent)
      self.StudentsTableFrame.pack(
        fill = "both",
        expand = True
      )

      for col, header in enumerate(self.headers):
        HeaderLabel = customtkinter.CTkLabel(self.StudentsTableFrame)
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
        self.StudentsTableFrame.columnconfigure(
          col,
          weight = 1
        )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)