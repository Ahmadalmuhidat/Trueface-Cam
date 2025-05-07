from app.config.configrations import Configrations

class DataManager:
  _instance = None

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(DataManager, cls).__new__(cls)
      cls._instance._init()
    return cls._instance

  def _init(self):
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