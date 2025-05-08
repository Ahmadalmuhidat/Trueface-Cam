from app.config.configrations import Configrations
from app.models import student, attendance, class_

class Data_Manager:
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self):
    # prevent re-initialization
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # global data
    self.current_class_students = []
    self.current_lecture_attendance = []
    self.current_lecture_attendance_report = []
    self.current_teacher_classes = []

    # global settings
    self.current_class = None
    self.start_time = None
    self.allowed_minutes = None
    self.current_teacher = None

    # auth
    self.token = None
    self.config = Configrations()

  def get_current_class_students(self):
    return self.current_class_students

  def set_current_class_students(self, current_class_students):
    self.current_class_students = [
      student.Student(
        data['ID'],
        data['FirstName'],
        data['MiddleName'],
        data['LastName'],
        data['Gender'],
        data['FaceID'],
        data['Createdate'],
      ) for data in current_class_students
    ]

  def get_current_lecture_attendance(self):
    return self.current_lecture_attendance
  
  def set_current_lecture_attendance(self, current_lecture_attendance):
    self.current_lecture_attendance = [
      attendance.Attendance(
        student.Student(
          data['ID'],
          data['FirstName'],
          data['MiddleName'],
          data['LastName']
        ),
        data['Time']
      ) for data in current_lecture_attendance
    ]

  def get_current_lecture_attendance_report(self):
    return self.current_lecture_attendance_report
  
  def set_current_lecture_attendance_report(self, current_lecture_attendance_report):
    self.current_lecture_attendance_report = current_lecture_attendance_report

  def get_current_teacher_classes(self):
    return self.current_teacher_classes
  
  def set_current_teacher_classes(self, current_teacher_classes):
    self.current_teacher_classes = [
      class_.Class(
        data['ID'],
        data['SubjectArea'],
        data['StartTime'],
        data['EndTime']
      ) for data in current_teacher_classes
    ]

  def get_current_class(self):
    return self.current_class
  
  def set_current_class(self, current_class):
    self.current_class = current_class

  def get_start_time(self):
    return self.start_time
  
  def set_start_time(self, start_time):
    self.start_time = start_time

  def get_allowed_minutes(self):
    return self.allowed_minutes

  def set_allowed_minutes(self, allowed_minutes):
    self.allowed_minutes = allowed_minutes

  def get_current_teacher(self):
    return self.current_teacher

  def set_current_teacher(self, current_teacher):
    self.current_teacher = current_teacher

  def get_token(self):
    return self.token
  
  def set_token(self, token):
    self.token = token

  def get_config(self):
    return self.config