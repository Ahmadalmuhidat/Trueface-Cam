from app.config.configrations import Configrations

class DataManager():
  Students = []
  Attendance = []
  Report = []
  cursor = None
  db = None
  current_class = None
  StartTime = None
  AllowedMinutes = None
  CurrentTeacher = None
  token = ""
  Classes = []
  ClassStudents = []

  config = Configrations()