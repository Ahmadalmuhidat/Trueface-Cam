import sys
import os
import mysql.connector
import json
import uuid

from Configrations import Configrations
from CTkMessagebox import CTkMessagebox
from datetime import datetime

class DatabaseManager(Configrations):
  cursor = None
  db = None
  CurrentClass = None
  CurrentTeacher = None
  Students = []
  Attendance = []

  def __init__(self) -> None:
    try:
      self.Classes = []

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
      DatabaseManager.db = mysql.connector.connect(
        host = self.Host,
        user = self.User,
        password = self.User,
        database = self.Database
      )

      DatabaseManager.cursor = DatabaseManager.db.cursor()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def checkUser(self, email, password):
    try:
        data = (email,)
        query = '''
        SELECT
          UserID,
          UserPassword
        FROM
          Users
        WHERE
          UserEmail=%s
        '''

        DatabaseManager.cursor.execute(query, data)
        User = DatabaseManager.cursor.fetchall()

        if len(User) == 1:
          if str(User[0][1]) == str(password):
            return User[0][0]
          else:
            CTkMessagebox(title="Info", message="Incorrect password")
            return False
        else:
          CTkMessagebox(title="Info", message="Email was not found")
          return False

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
      SELECT
        LicenseStatus
      FROM
        Customers
      WHERE
        LicenseActivationKey=%s
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
      data = (DatabaseManager.CurrentClass,)
      query = '''
        SELECT
          Attendance.AttendanceTime,
          Students.StudentID,
          Students.StudentFirstName,
          Students.StudentMiddleName,
          Students.StudentLastName,
        FROM
          Attendance
        LEFT JOIN
          Students
        ON
          Attendance.AttendanceStudentID = Students.StudentID
        WHERE
          Attendance.AttendanceDate = CURDATE()
        AND
          Attendance.AttendanceClassID = %s
      '''

      DatabaseManager.cursor.execute(query, data)
      DatabaseManager.Attendance = DatabaseManager.cursor.fetchall()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def getClasses(self):
    try:
      data = (DatabaseManager.CurrentTeacher,)
      query = '''
        SELECT
          ClasseID,
          ClassSubjectArea,
          ClasseSessionStartTime,
          ClasseSessionEndTime
        FROM
           Classes
        WHERE
          ClasseInstructorID=%s
      '''

      DatabaseManager.cursor.execute(query, data)
      self.Classes = DatabaseManager.cursor.fetchall()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def checkAttendance(self, StudentID):
    try:
      data = (StudentID, DatabaseManager.CurrentClass)
      query = '''
        SELECT *
        FROM
          Attendance
        WHERE
          AttendanceDate = CURDATE()
        AND
          AttendanceStudentID=%s
        AND
          AttendanceClassID=%s
      '''

      DatabaseManager.cursor.execute(query, data)
      result = DatabaseManager.cursor.fetchall()
      DatabaseManager.db.commit()

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

  def insertAttendance(self, StudentID):
    try:
      if not self.checkAttendance(StudentID):
        now = datetime.now()

        AttendanceID = str(uuid.uuid4())
        date  = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        data = (AttendanceID, StudentID, DatabaseManager.CurrentClass, time, date)

        query = "INSERT INTO Attendance VALUES (%s, %s, %s, %s, %s)"
        DatabaseManager.cursor.execute(query, data)
        DatabaseManager.db.commit()

        CTkMessagebox(title="Match Found", message="{} has been signed".format(StudentID), icon="check")
      else:
        CTkMessagebox(title="Info", message="{} has been already signed".format(StudentID))

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def getStudents(self):
    try:
      query = "SELECT * FROM Students"
      DatabaseManager.cursor.execute(query)
      DatabaseManager.Students = DatabaseManager.cursor.fetchall()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass