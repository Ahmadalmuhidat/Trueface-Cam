class Student:
  def __init__(self, student_id, first_name, middle_name, last_name, geneder = None, face_encode = None, create_date = None):
    self._student_id = student_id
    self._first_name = first_name
    self._middle_name = middle_name
    self._last_name = last_name
    self._gender = geneder
    self._face_encode = face_encode
    self._create_date = create_date
  
  def get_student_id(self):
    return self._student_id
  
  def get_first_name(self):
    return self._first_name

  def get_middle_name(self):
    return self._middle_name

  def get_last_name(self):
    return self._last_name

  def get_gender(self):
    return self._gender

  def get_face_encode(self):
    return self._face_encode

  def get_create_date(self):
    return self._create_date