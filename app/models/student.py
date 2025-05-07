class Student:
  def __init__(self, student_id, first_name, middle_name, last_name, geneder = None, face_encode = None, create_date = None):
    self.student_id = student_id
    self.first_name = first_name
    self.middle_name = middle_name
    self.last_name = last_name
    self.gender = geneder
    self.face_encode = face_encode
    self.create_date = create_date
  
  def get_student_id(self):
    return self.student_id
  
  def get_first_name(self):
    return self.first_name

  def get_middle_name(self):
    return self.middle_name

  def get_last_name(self):
    return self.last_name

  def get_gender(self):
    return self.gender

  def get_face_encode(self):
    return self.face_encode

  def get_create_date(self):
    return self.create_date