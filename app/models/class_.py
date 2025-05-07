class Class:
  def __init__(self, class_id, subject_area, start_time, end_time):
    self.class_id = class_id
    self.subject_area = subject_area
    self.start_time = start_time
    self.end_time = end_time
  
  def get_class_id(self):
    return self.class_id
  
  def get_subject_area(self):
    return self.subject_area
  
  def get_start_time(self):
    return self.start_time
  
  def get_end_time(self):
    return self.end_time