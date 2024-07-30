import os
import sys

class Configrations:
  CloseThreads = False

  def __init__(self) -> None:
    try:
      self.Host = None
      self.User = None
      self.Password = None
      self.Database = None
      self.ActivationKey = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
  
  def GetSettings(self):
    try:
      self.Host = "timewizeai.mysql.database.azure.com"
      self.User = "timewizeai"
      self.Password = "system@admin99"
      self.Database = "TimeWizeAI"
      self.ActivationKey = "1234"

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass