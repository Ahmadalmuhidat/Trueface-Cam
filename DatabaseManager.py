import os
import sys
import mysql.connector
import uuid
import requests
import json

from Configrations import Configrations
from CTkMessagebox import CTkMessagebox
from datetime import datetime, date

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

  def __init__(self) -> None:
    try:
      self.Classes = []
      self.ClassStudents = []

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
  
  def ReturnCursor(self):
    try:
      return DatabaseManager.cursor

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Connect(self):
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

  def CheckUser(self, email, password):
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

        DatabaseManager.cursor = DatabaseManager.db.cursor()

        DatabaseManager.cursor.execute(query, data)
        User = DatabaseManager.cursor.fetchall()

        DatabaseManager.cursor.close()

        if len(User) == 1:
          if str(User[0][1]) == str(password):
            return User[0][0]
          else:
            CTkMessagebox(
              title = "Info",
              message = "Incorrect password"
            )
            return False
        else:
          CTkMessagebox(
            title = "Info",
            message = "Email was not found"
          )
          return False

    except Exception as e: 
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(exc_obj)

  def checkLicenseStatus(self):
    try:
      data = {
        "License": self.ActivationKey
      }
      response = requests.get(
        "https://timewizeai-license-api.azurewebsites.net/check_license",
        data
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
  def GetAttendance(self):
    try:
      data = (
        DatabaseManager.CurrentClass,
        date.today()
      )
      query = '''
        SELECT
          Students.StudentID,
          Students.StudentFirstName,
          Students.StudentMiddleName,
          Students.StudentLastName,
          TIME_FORMAT(Attendance.AttendanceTime, '%H:%i') AS AttendanceTime
        FROM
          Attendance
        LEFT JOIN
          Students
        ON
          Attendance.AttendanceStudentID = Students.StudentID
        WHERE
          Attendance.AttendanceClassID = %s
        AND
          Attendance.AttendanceDate = %s
      '''

      DatabaseManager.cursor = DatabaseManager.db.cursor()

      DatabaseManager.cursor.execute(query, data)
      DatabaseManager.Attendance = DatabaseManager.cursor.fetchall()

      DatabaseManager.cursor.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetReport(self, StartTime, AllowedMinutes):
    try:
      data = (
        StartTime,
        int (AllowedMinutes) * 60,
        DatabaseManager.CurrentClass,
        date.today()
      )
      query = '''
        SELECT
          Students.StudentID,
          Students.StudentFirstName,
          Students.StudentMiddleName,
          Students.StudentLastName,
          CASE
            WHEN Attendance.AttendanceTime IS NULL THEN 'absent'
            ELSE TIME_FORMAT(Attendance.AttendanceTime, '%H:%i')
          END AS AttendanceTime,
          CASE
            WHEN Attendance.AttendanceTime IS NULL THEN FALSE
            WHEN TIME_TO_SEC(TIMEDIFF(Attendance.AttendanceTime, %s)) > %s THEN 'late'
            ELSE 'not late'
          END AS Lateness
        FROM
          Students
        LEFT JOIN
          Attendance
        ON
          Attendance.AttendanceStudentID = Students.StudentID
        AND
          Attendance.AttendanceClassID = %s
        AND
          Attendance.AttendanceDate = %s
        '''

      DatabaseManager.cursor = DatabaseManager.db.cursor()

      DatabaseManager.cursor.execute(query, data)
      DatabaseManager.Report = DatabaseManager.cursor.fetchall()

      DatabaseManager.cursor.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def SearchAttendance(self, term):
    try:
      data = (
        term,
        date.today()
      )
      query = '''
        SELECT
          Attendance.AttendanceTime,
          Students.StudentID,
          Students.StudentFirstName,
          Students.StudentMiddleName,
          Students.StudentLastName
        FROM
          Attendance
        LEFT JOIN
          Students
        ON
          Attendance.AttendanceStudentID = Students.StudentID
        WHERE
          Attendance.AttendanceStudentID = %s
        AND
          Attendance.AttendanceDate = %s
      '''

      DatabaseManager.cursor = DatabaseManager.db.cursor()

      DatabaseManager.cursor.execute(query, data)
      DatabaseManager.Attendance = DatabaseManager.cursor.fetchall()

      DatabaseManager.cursor.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetClasses(self):
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

      DatabaseManager.cursor = DatabaseManager.db.cursor()

      DatabaseManager.cursor.execute(query, data)
      self.Classes = DatabaseManager.cursor.fetchall()

      DatabaseManager.cursor.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def CheckAttendance(self, StudentID):
    try:
      data = (
        date.today(),
        StudentID,
        DatabaseManager.CurrentClass
      )
      query = '''
        SELECT *
        FROM
          Attendance
        WHERE
          AttendanceDate = %s
        AND
          AttendanceStudentID=%s
        AND
          AttendanceClassID=%s
      '''

      DatabaseManager.cursor = DatabaseManager.db.cursor()

      DatabaseManager.cursor.execute(query, data)
      result = DatabaseManager.cursor.fetchall()
      DatabaseManager.db.commit()

      DatabaseManager.cursor.close()

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

  def InsertAttendance(self, StudentID, StudentName):
    try:
      if not self.CheckAttendance(StudentID):
        now = datetime.now()
        AttendanceID = str(uuid.uuid4())
        date  = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        data = (
          AttendanceID,
          StudentID,
          DatabaseManager.CurrentClass,
          time,
          date
        )

        DatabaseManager.cursor = DatabaseManager.db.cursor()

        query = "INSERT INTO Attendance VALUES (%s, %s, %s, %s, %s)"
        DatabaseManager.cursor.execute(query, data)
        DatabaseManager.db.commit()

        DatabaseManager.cursor.close()

        CTkMessagebox(
          title = "Match Found",
          message = "{} has been signed".format(StudentName),
          icon = "check"
        )
      else:
        CTkMessagebox(
          title = "Info",
          message = "{} has been already signed".format(StudentName)
        )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetStudents(self):
    try:

      days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
      }
      today = days[date.today().weekday()]
    
      DatabaseManager.cursor = DatabaseManager.db.cursor()

      data = (
        DatabaseManager.CurrentClass,
        today
      )
      query = '''
        SELECT
          Students.*      
        FROM
          Students
        JOIN
          ClassStudentRelation
        ON
          ClassStudentRelation.StudentID = Students.StudentID
        WHERE
          ClassStudentRelation.ClassID = %s
        AND
          ClassStudentRelation.ClassDay = %s
      '''

      DatabaseManager.cursor.execute(query, data)
      DatabaseManager.Students = DatabaseManager.cursor.fetchall()

      DatabaseManager.cursor.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def GetClassStudents(self):
    try:

      days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
      }
      today = days[date.today().weekday()]
    
      DatabaseManager.cursor = DatabaseManager.db.cursor()

      data = (
        DatabaseManager.CurrentClass,
        today
      )
      query = '''
        SELECT
          Students.StudentID,
          Students.StudentFirstName,
          Students.StudentMiddleName,
          Students.StudentLastName,
          Students.StudentGender  
        FROM
          Students
        JOIN
          ClassStudentRelation
        ON
          ClassStudentRelation.StudentID = Students.StudentID
        WHERE
          ClassStudentRelation.ClassID = %s
        AND
          ClassStudentRelation.ClassDay = %s
      '''

      DatabaseManager.cursor.execute(query, data)
      self.ClassStudents = DatabaseManager.cursor.fetchall()

      DatabaseManager.cursor.close()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass