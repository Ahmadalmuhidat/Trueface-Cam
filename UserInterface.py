import os
import sys
import customtkinter
import pages.Home as Home
import pages.Attendance as Attendance
import pages.Settings as Settings
import pages.Students as Students

from CameraManager import CameraManager
from DatabaseManager import DatabaseManager
from Configrations import Configrations

class UserInterface(CameraManager):
  def __init__(self, UserID):
    try:
      super().__init__()

      DatabaseManager.CurrentTeacher = UserID

      self.CurrentPage = None
      self.pages = {}

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Navbar(self, window):
    try:
      navbar = customtkinter.CTkFrame(window)
      navbar.pack(fill=customtkinter.X)

      HomeButton = customtkinter.CTkButton(navbar)
      HomeButton.configure(
        corner_radius = 0,
        command = lambda: self.ShowPage("Home"),
        text = "Home"
      )
      HomeButton.pack(side = customtkinter.LEFT)

      AttendanceButton = customtkinter.CTkButton(navbar)
      AttendanceButton.configure(
        corner_radius = 0,
        command = lambda: self.ShowPage("Attendance"),
        text = "Attendance"
      )
      AttendanceButton.pack(side = customtkinter.LEFT)

      StudentsButton = customtkinter.CTkButton(navbar)
      StudentsButton.configure(
        corner_radius = 0,
        command = lambda: self.ShowPage("Students"),
        text = "Students"
      )
      StudentsButton.pack(side = customtkinter.LEFT)

      SettingsButton = customtkinter.CTkButton(navbar)
      SettingsButton.configure(
        corner_radius = 0,
        command = lambda: self.ShowPage("Settings"),
        text = "Settings"
      )
      SettingsButton.pack(side = customtkinter.LEFT)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def ShowPage(self, name):
    try:
      if self.CurrentPage:
        self.CurrentPage.pack_forget()

      self.CurrentPage = self.pages[name]
      self.CurrentPage.pack(fill=customtkinter.BOTH, expand=True)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def CreatePage(self, window, name):
    try:
      page = customtkinter.CTkFrame(window)
      self.pages[name] = page

      if name == "Home":
        Home.Home().Create(page)
      elif name == "Attendance":
        Attendance.Attendance().Create(page)
      elif name == "Settings":
        Settings.Settings().Create(page)
      elif name == "Students":
        Students.Students().Create(page)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def OnClosing(self):
    try:
      if self.ReturnActivateCapturing():
        self.StopCapturing()

      self.window.destroy()

      Configrations.CloseThreads = True

      sys.exit(0)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def StartTheProgram(self):
    try:
      self.window = customtkinter.CTk()
      
      width =  self.window.winfo_screenwidth()
      height =  self.window.winfo_screenheight()
      self.window.geometry("%dx%d" % (width, height))

      self.window.title("TimeWizeAI Camera")

      self.window.protocol("WM_DELETE_WINDOW", self.OnClosing)

      self.Navbar(self.window)
      self.CreatePage(self.window, "Home")
      self.CreatePage(self.window, "Attendance")
      self.CreatePage(self.window, "Settings")
      self.CreatePage(self.window, "Students")

      self.ShowPage("Home")

      self.window.mainloop()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
    except KeyboardInterrupt:
      pass