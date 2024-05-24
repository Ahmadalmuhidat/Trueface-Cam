import customtkinter
import os
import sys
import pages.Home as Home
import pages.Attendance as Attendance
import threading

from CameraManager import CameraManager

class UserInterface(CameraManager):
  def __init__(self):
    try:
      super().__init__()

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

      HomeButton = customtkinter.CTkButton(navbar, text="Home")
      HomeButton.configure(corner_radius=0, command=lambda: self.showPage("Home"))
      HomeButton.pack(side=customtkinter.LEFT)

      AttendanceButton = customtkinter.CTkButton(navbar, text="Attendance")
      AttendanceButton.configure(corner_radius=0, command=lambda: self.showPage("Attendance"))
      AttendanceButton.pack(side=customtkinter.LEFT)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def showPage(self, name):
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

  def createPage(self, window, name):
    try:
      page = customtkinter.CTkFrame(window)
      self.pages[name] = page

      if name == "Home":
        Home.Home().create(page)
      elif name == "Attendance":
        Attendance.Attendance().create(page)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def onClosing(self):
    try:
      if self.returnActivateCapturing():
        self.stopCapturing()

      self.window.destroy()
      threadsToTerminate = [thread for thread in threading.enumerate() if thread.ident != threading.get_ident()]

      for thread in threadsToTerminate:
        if thread.is_alive():
          thread.join(timeout=1)
      
      print("Done Closing")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
    finally:
      sys.exit(0)

  def startTheProgram(self):
    try:
      self.window = customtkinter.CTk()
      self.window.geometry("1100x950")
      self.window.resizable(width=0, height=0)
      self.window.title("TimeWizeAI Camera")

      self.window.protocol("WM_DELETE_WINDOW", self.onClosing)

      self.Navbar(self.window)
      self.createPage(self.window, "Home")
      self.createPage(self.window, "Attendance")

      self.showPage("Home")

      self.window.mainloop()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
    except KeyboardInterrupt:
      pass

if __name__ ==  "__main__":
  IndividualsFaceDetector = UserInterface()
  IndividualsFaceDetector.startTheProgram()