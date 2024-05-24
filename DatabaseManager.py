import mysql.connector
import sys
import os
import json
import uuid

from CTkMessagebox import CTkMessagebox
from datetime import datetime

class DatabaseManager:
  cursor = None

  def __init__(self) -> None:
    try:
      self.Individuals = []
      self.Attendance = []

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
  
  def returnCursor(self):
    try:
      return DatabaseManager.cursor

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def connect(self):
    try:
      with open("configrations.json", 'r') as json_file:
        config = json.load(json_file)["Database"]

      self.db = mysql.connector.connect(
        host = config["host"],
        user = config["user"],
        password = config["password"],
        database = config["database"]
      )

      DatabaseManager.cursor = self.db.cursor()

    except Exception as e: 
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  
  def checkCustomerLicenseStatus(self):
    try:
      with open('configrations.json', 'r') as file:
        ActivationKey = json.load(file)['Activation_Key']

      data = (ActivationKey,)
      query = '''
      SELECT CustomerLicenseStatus
      FROM Customers
      WHERE CustomerActivationKey=%s
      '''

      DatabaseManager.cursor.execute(query, data)
      CustomerLicenseStatus = DatabaseManager.cursor.fetchall()

      if len(CustomerLicenseStatus) > 0:
        if CustomerLicenseStatus[0][0] == "inactive":
          title="License not active"
          message="Please Renew your License"
          icon="cancel"
          msg = CTkMessagebox(title=title, message=message,icon=icon, option_1="ok")
          response = msg.get()

          if response=="ok":
            sys.exit(0)     
      else:
          title="License not found"
          message="The Activation Key is not valid, please contact the technical team"
          icon="cancel"
          msg = CTkMessagebox(title=title, message=message,icon=icon, option_1="ok")
          response = msg.get()

          if response=="ok":
            sys.exit(0)     

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def getAttendance(self):
    try:
      with open('configrations.json', 'r') as file:
        WorkingHourStart = json.load(file)['Working_Hours']['start']

      data = [WorkingHourStart]
      query = '''
          SELECT AttendanceIndividual, AttendanceDate, AttendanceTime
          FROM Attendance
          WHERE TIME(AttendanceTime) > %s
          AND AttendanceDate = CURDATE()
      '''
      DatabaseManager.cursor.execute(query, data)
      self.Attendance = DatabaseManager.cursor.fetchall()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def checkAttendance(self, name):
    try:
      data = (name,)
      query = '''
      SELECT * FROM
      Attendance
      WHERE AttendanceDate = CURDATE()
      AND AttendanceIndividual=%s
      '''

      DatabaseManager.cursor.execute(query, data)
      result = DatabaseManager.cursor.fetchall()
      self.db.commit()

      if len(result) > 0:
        return True
      else:
        return False

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def insertAttendance(self, name):
    try:
      if not self.checkAttendance(name):
        now = datetime.now()
        id = str(uuid.uuid4())
        date  = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        data = (id, name, date, time)

        query = "INSERT INTO Attendance VALUES (%s, %s, %s, %s)"
        DatabaseManager.cursor.execute(query, data)
        self.db.commit()

        CTkMessagebox(title="Match Found", message="{} has been signed".format(name), icon="check")
      else:
        CTkMessagebox(title="Info", message="{} has been already signed".format(name))

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def getIndividuals(self):
    try:
      query = "SELECT * FROM Individuals"
      DatabaseManager.cursor.execute(query)
      self.Individuals = DatabaseManager.cursor.fetchall()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass