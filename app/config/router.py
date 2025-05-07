import os
import sys
import customtkinter

from app.config.configrations import Configrations

class Router:
  def __init__(self):
    self._current_page = None
    self._config = Configrations()

  def clear_window(self):
    if self._current_page:
      self._current_page.pack_forget()
  
  def get_current_page(self):
    return self._current_page
  
  def get_router_configrations(self):
    return self._config

  def navigate(self, view_class):
    try:
      self.clear_window()

      self._config.window.configure(cursor="watch")
      self._config.window.update()

      frame = customtkinter.CTkFrame(self._config.window)
      view_instance = view_class()

      self._config.window.configure(cursor="")
      self._config.window.update()

      view_instance.lunch_view(frame)

      self._current_page = frame
      self._current_page.pack(fill="both", expand=True)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass