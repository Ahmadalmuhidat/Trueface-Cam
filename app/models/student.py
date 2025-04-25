class Student:
  def __init__(self, student_id, first_name, middle_name, last_name, geneder = None, face_encode = None, create_date = None):
    self.id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = geneder
    self.face_encode = face_encode
    self.create_date = create_date