import os
import sys
import customtkinter

from DatabaseManager import DatabaseManager
from CTkMessagebox import CTkMessagebox
from CameraManager import CameraManager

class Settings(CameraManager):
  def __init__(self):
    try:
      super().__init__()

      self.GetSettings()
      self.GetClasses()

      self.class_id_title_map = {
        f"{x[1]} {x[2]}-{x[3]}": x[0] for x in self.Classes
      }
      
      self.class_start_time_map = {
        f"{x[1]} {x[2]}-{x[3]}": x[2] for x in self.Classes
      }
      
      self.cameras_key_map = {
        value: key for key, value in CameraManager.AvailableCameras.items()
      }

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  
  def UpdateCurrentCamerass(self, choise):
    try:
      self.UpdateCurrentCamera(
        self.cameras_key_map[choise]
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  
  def UpdateSettings(self):
    try:
      if not self.CurrentLectureEntry.get():
        title = "Missing Entries"
        message="Please Select Current Lecture"
        icon="cancel"
        CTkMessagebox(
          title = title,
          message = message,
          icon = icon
        )
        return

      if not self.AllowedMinutesEntry.get():
        title = "Missing Entries"
        message="Please Enter Allowed Late Time"
        icon="cancel"
        CTkMessagebox(
          title = title,
          message = message,
          icon = icon
        )
        return

      DatabaseManager.CurrentClass = self.class_id_title_map[
        self.CurrentLectureEntry.get()
      ]
      DatabaseManager.StartTime = self.class_start_time_map[
        self.CurrentLectureEntry.get()
      ]
      DatabaseManager.AllowedMinutes = self.AllowedMinutesEntry.get()
      # threading.Thread(target=self.checkCustomerLicenseStatus).start()

      self.GetStudents()
      self.GetAttendance()

      title = "Info"
      message="Settings has been updated"
      icon="check"
      CTkMessagebox(
        title = title,
        message = message,
        icon = icon
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Create(self, parent):
    try:
      ContentFrame = customtkinter.CTkFrame(parent)
      ContentFrame.pack(
        padx = 20,
        pady = 20
      )

      CurrentLecturelabel = customtkinter.CTkLabel(ContentFrame)
      CurrentLecturelabel.grid(
        row = 5,
        column = 0,
        padx = 10,
        pady = 10
      )
      CurrentLecturelabel.configure(text = "Current Lecture:")

      self.CurrentLectureEntry = customtkinter.CTkComboBox(ContentFrame)
      self.CurrentLectureEntry.grid(
        row = 5,
        column = 1,
        padx = 10,
        pady = 10
      )
      self.CurrentLectureEntry.configure(
        values = [f"{x[1]} {x[2]}-{x[3]}" for x in self.Classes],
        width = 400
      )
      self.CurrentLectureEntry.set("None")

      AllowedMinuteslabel = customtkinter.CTkLabel(
        ContentFrame,
        text = "Allowed Minutes:"
      )
      AllowedMinuteslabel.grid(
        row = 6,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.AllowedMinutesEntry = customtkinter.CTkEntry(
        ContentFrame,
        width = 400
      )
      self.AllowedMinutesEntry.grid(
        row = 6,
        column = 1,
        padx = 10,
        pady = 10
      )

      AvailableCameraslabel = customtkinter.CTkLabel(
        ContentFrame,
        text = "Available Cameras:"
      )
      AvailableCameraslabel.grid(
        row = 7,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.AvailableCamerasEntry = customtkinter.CTkComboBox(ContentFrame)
      self.AvailableCamerasEntry.grid(
        row = 7,
        column = 1,
        padx = 10,
        pady = 10
      )
      self.AvailableCamerasEntry.configure(
        values = list(self.cameras_key_map.keys()),
        width = 400,
        command = self.UpdateCurrentCamerass
      )
      self.AvailableCamerasEntry.set(
        "None"
      )

      ViewCameraButton = customtkinter.CTkButton(ContentFrame)
      ViewCameraButton.grid(
        row = 8,
        columnspan = 2,
        padx = 10,
        pady = 10,
        sticky = "nsew",
      )
      ViewCameraButton.configure(
        text = "Test Current Camera",
        command = self.viewCam
      )

      SaveButton = customtkinter.CTkButton(ContentFrame)
      SaveButton.grid(
        row = 9,
        columnspan = 2,
        padx = 10,
        pady = 10,
        sticky = "nsew",
      )
      SaveButton.configure(
        text = "Update Settings",
        command = self.UpdateSettings
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)