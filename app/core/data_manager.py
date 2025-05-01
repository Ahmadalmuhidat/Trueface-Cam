from app.config.configrations import Configrations

class DataManager():
  # global data
  current_class_students = []
  current_lecture_attendance = []
  current_lecture_attendance_report = []
  current_teacher_classes = []

  # global settings
  current_class = None
  start_time = None
  allowed_minutes = None
  current_teacher = None
  
  # auth
  token = None

  config = Configrations()