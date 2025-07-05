import os
import sys
import customtkinter

import app.views.Login as Login
import app.views.Home as Home
import app.views.Attendance as Attendance
import app.views.Settings as Settings
import app.views.Students as Students

from app.config.configrations import Configrations
from app.core.camera_module import Camera_Manager_Module
from CTkMessagebox import CTkMessagebox
from app.config.router import Router

class Main():
  def __init__(self):
    try:
      self._config = Configrations()
      self._camera_manager = Camera_Manager_Module()
      self._router = Router()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      FileName = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, FileName, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def create_navbar(self):
    try:
      navbar = customtkinter.CTkFrame(self.window)
      navbar.pack(fill=customtkinter.X)

      home_view = customtkinter.CTkButton(
        navbar,
        corner_radius = 0,
        command = lambda: self._router.navigate(Home.Home),
        text = "Home"
      )
      home_view.pack(side = customtkinter.LEFT)

      attendance_view = customtkinter.CTkButton(
        navbar,
        corner_radius = 0,
        command = lambda: self._router.navigate(Attendance.Attendance),
        text = "Attendance"
      )
      attendance_view.pack(side = customtkinter.LEFT)

      students_view = customtkinter.CTkButton(
        navbar,
        corner_radius = 0,
        command = lambda: self._router.navigate(Students.Students),
        text = "Students"
      )
      students_view.pack(side = customtkinter.LEFT)

      settings_view = customtkinter.CTkButton(
        navbar,
        corner_radius = 0,
        command = lambda: self._router.navigate(Settings.Settings),
        text = "Settings"
      )
      settings_view.pack(side = customtkinter.LEFT)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def when_app_close(self):
    try:
      if self._camera_manager.get_activate_capturing():
        title = "Error"
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = "Please stop the camera first",
          icon = icon
        )
        return

      self.window.destroy()
      sys.exit(0)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def start_program(self):
    try:
      self.window = customtkinter.CTk()

      self._config.set_window(self.window)
      self._camera_manager.get_working_cameras()
    
      width = self.window.winfo_screenwidth()
      height = self.window.winfo_screenheight()
      self.window.geometry("%dx%d" % (width, height))
      self.window.iconbitmap("logo.ico")

      self.window.title("TrueFace Camera")

      self.window.protocol(
        "WM_DELETE_WINDOW",
        self.when_app_close
      )

      self.create_navbar()
      self._router.navigate(Home.Home)

      self.window.mainloop()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
    except KeyboardInterrupt:
      pass

if __name__ == "__main__":
  # Main().start_program()
  Login.Login().lunch_view()