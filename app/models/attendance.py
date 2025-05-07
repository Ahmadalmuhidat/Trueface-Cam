from app.models.student import Student

class Attendance:
  def __init__(self, student: Student, time):
    self.student = student
    self.time = time
  
  def get_student(self):
    return self.student
  
  def get_time(self):
    return self.time