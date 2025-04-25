import sys
import os
import customtkinter

class Router:
  def __init__(self):
    self.current_page = None

  def clear_window(self):
    if self.current_page:
      self.current_page.pack_forget()

  def navigate(self, view_class):
    self.clear_window()

    Configrations.window.configure(cursor="watch")
    Configrations.window.update()

    frame = customtkinter.CTkFrame(Configrations.window)
    view_instance = view_class()

    Configrations.window.configure(cursor="")
    Configrations.window.update()

    view_instance.lunch_view(frame)

    self.current_page = frame
    self.current_page.pack(fill="both", expand=True)

class Configrations:
  window = None

  def __init__(self) -> None:
    try:
      self.BaseURL = "http://localhost:8000"
      self.router = Router()
      self.token = ""

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass
  
  def set_window(self, window):
    try:
      Configrations.window = window

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def get_base_url(self):
    try:
      return self.BaseURL

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass