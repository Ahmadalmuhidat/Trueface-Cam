class Class:
  def __init__(self, class_id, subject_area, start_time, end_time):
    self._class_id = class_id
    self._subject_area = subject_area
    self._start_time = start_time
    self._end_time = end_time
  
  def get_class_id(self):
    return self._class_id
  
  def get_subject_area(self):
    return self._subject_area
  
  def get_start_time(self):
    return self._start_time
  
  def get_end_time(self):
    return self._end_time