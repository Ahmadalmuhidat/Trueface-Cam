import os
import sys
import requests
# import winsound
import json

from Configrations import Configrations
from CTkMessagebox import CTkMessagebox

class DatabaseManager(Configrations):
  Students = []
  Attendance = []
  Report = []
  cursor = None
  db = None
  CurrentClass = None
  StartTime = None
  AllowedMinutes = None
  CurrentTeacher = None
  token = ""

  def __init__(self) -> None:
    try:
      self.BaseURL = "http://localhost:8000"
      self.Classes = []
      self.ClassStudents = []

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def CheckUser(self, email, password):
    try:
      data = {
        "email": email,
        "password": password
      }
      response = requests.get(
        self.BaseURL + "/teacher/check_user",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        return response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while checking user info",
          icon = icon
        )
  
    except Exception as e: 
        ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
        fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
        print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
        print(ExceptionObject)

  def GetCurrentClassAttendance(self):
    try:
      data = {
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/teacher/get_current_class_attendance",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        DatabaseManager.Attendance = response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while getting the attendance",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def GetReport(self, StartTime, AllowedMinutes):
    try:
      data = {
        "StartTime": StartTime,
        "AllowedMinutes": AllowedMinutes,
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/teacher/get_report",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        DatabaseManager.Report = response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while getting the report",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def SearchAttendance(self, StudentID):
    try:
      data = {
        "StudentID": StudentID,
      }
      response = requests.get(
        self.BaseURL + "/teacher/search_attendance",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        DatabaseManager.Attendance = response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while searching in the attendance",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def GetCurrentTeacherClasses(self):
    try:
      data = {
        "CurrentTeacher": DatabaseManager.token
      }
      response = requests.get(
        self.BaseURL + "/teacher/get_current_teacher_classes",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        self.Classes = response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while getting the classes",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def CheckAttendance(self, StudentID):
    try:
      data = {
        "StudentID": StudentID,
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/teacher/check_attendance",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        return response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while checking student attendance",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def InsertAttendance(self, StudentID, StudentName):
    try:
      if not self.CheckAttendance(StudentID):
        data = {
          "StudentID": StudentID,
          "CurrentClass": DatabaseManager.CurrentClass
        }
        response = requests.post(
          self.BaseURL + "/teacher/insert_attendance",
          params = data
        ).content
        response = json.loads(response.decode('utf-8'))

        if response.get("status_code") == 200:
          frequency = 2500
          duration = 500  # 1 second
          # winsound.Beep(
          #   frequency,
          #   duration
          # )
          CTkMessagebox(
            title = "Match Found",
            message = "{} has been signed".format(StudentName),
            icon = "check"
          )
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while inserting attendance",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def GetStudentsWithFaceEncode(self):
    try:
      data = {
        "CurrentClass": DatabaseManager.CurrentClass,
      }
      response = requests.get(
        self.BaseURL + "/teacher/get_students_with_face_encode",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        DatabaseManager.Students = response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while getting the students",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def GetClassStudents(self):
    try:
      data = {
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/teacher/get_class_students",
        params = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        self.ClassStudents = response.get("data")
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while getting the students",
          icon = icon
        )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass