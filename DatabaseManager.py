import os
import sys
import requests
import json

from Configrations import Configrations
from CTkMessagebox import CTkMessagebox

class DatabaseManager(Configrations):
  cursor = None
  db = None
  CurrentClass = None
  StartTime = None
  AllowedMinutes = None
  CurrentTeacher = None
  Students = []
  Attendance = []
  Report = []
  token = ""

  def __init__(self) -> None:
    try:
      # self.BaseURL = "https://timewizeai-license-api.azurewebsites.net"
      self.BaseURL = "http://192.168.1.112:8000"
      self.Classes = []
      self.ClassStudents = []

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def CheckUser(self, email, password):
    try:
      data = {
        "email": email,
        "password": password
      }
      response = requests.get(
        self.BaseURL + "/check_user",
        params = data
      ).content
      response_str = response.decode('utf-8')

      token =  json.loads(response_str)

      if token:
        DatabaseManager.token = token
        return True

    except Exception as e: 
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(exc_obj)

  def CheckLicenseStatus(self):
    try:
      data = {
        "License": self.ActivationKey
      }
      response = requests.get(
         "https://timewizeai-license-api.azurewebsites.net/check_license",
        params = data
      ).content
      response_str = response.decode('utf-8')

      if not json.loads(response_str):
          title = "License not active"
          message = "Please Renew your License"
          icon = "cancel"
          msg  =  CTkMessagebox(
            title = title,
            message = message,
            icon = icon,
            option_1 = "ok"
          )
          response = msg.get()

          if response == "ok":
            sys.exit(0)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetCurrentClassAttendance(self):
    try:
      data = {
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/get_current_class_attendance",
        params = data
      ).content
      response_str = response.decode('utf-8')

      DatabaseManager.Attendance = json.loads(response_str)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetReport(self, StartTime, AllowedMinutes):
    try:
      data = {
        "StartTime": StartTime,
        "AllowedMinutes": AllowedMinutes,
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/get_report",
        params = data
      ).content
      response_str = response.decode('utf-8')

      DatabaseManager.Report = json.loads(response_str)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def SearchAttendance(self, StudentID):
    try:
      data = {
        "StudentID": StudentID,
      }
      response = requests.get(
        self.BaseURL + "/search_attendance",
        params = data
      ).content
      response_str = response.decode('utf-8')

      DatabaseManager.Attendance = json.loads(response_str)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetCurrentTeacherClasses(self):
    try:
      data = {
        "CurrentTeacher": DatabaseManager.token
      }
      response = requests.get(
        self.BaseURL + "/get_current_teacher_classes",
        params = data
      ).content
      response_str = response.decode('utf-8')

      self.Classes = json.loads(response_str)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def CheckAttendance(self, StudentID):
    try:
      data = {
        "StudentID": StudentID,
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/check_attendance",
        params = data
      ).content
      response_str = response.decode('utf-8')

      result = json.loads(response_str)
      return result

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def InsertAttendance(self, StudentID, StudentName):
    try:
      if not self.CheckAttendance(StudentID):
        data = {
          "StudentID": StudentID,
          "CurrentClass": DatabaseManager.CurrentClass
        }
        response = requests.post(
          self.BaseURL + "/insert_attendance",
          params = data
        ).content
        response_str = response.decode('utf-8')
        
        if response_str:
          CTkMessagebox(
            title = "Match Found",
            message = "{} has been signed".format(StudentName),
            icon = "check"
          )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetStudentsWithFaceEncode(self):
    try:
      data = {
        "CurrentClass": DatabaseManager.CurrentClass,
      }
      response = requests.get(
        self.BaseURL + "/get_students_with_face_encode",
        params = data
      ).content
      response_str = response.decode('utf-8')

      DatabaseManager.Students = json.loads(response_str)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetClassStudents(self):
    try:
      data = {
        "CurrentClass": DatabaseManager.CurrentClass
      }
      response = requests.get(
        self.BaseURL + "/get_class_students",
        params = data
      ).content
      response_str = response.decode('utf-8')

      self.ClassStudents = json.loads(response_str)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass