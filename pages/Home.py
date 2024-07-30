import os
import sys
import customtkinter
import psutil
import time
import threading

from FaceRecognitionModal import FaceRecognitionModal
from DatabaseManager import DatabaseManager
from Configrations import Configrations

class Home(FaceRecognitionModal):
  def __init__(self):
    try:
      super().__init__()

      self.GetSettings()
      self.Connect()
      # self.checkLicenseStatus()
      self.ListWorkingCameras()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def UpdateCamerasStatus(self):
    try:
      if self.CameraActive:
        self.CameraStatus.configure(
          text = "Connected",
          text_color = "green"
        )
      else:
        self.CameraStatus.configure(
          text= "Disconnected",
          text_color = "red"
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def UpdateDatabaseStatus(self):
    try:
      self.DatabaseStatus.configure(
        text = "Connected",
        text_color = "green"
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass 

  def UpdateCPUMetrics(self):
    try:
      while True:
        metrics = psutil.cpu_percent(interval=1)
        self.CPUCount.configure(
          text = "CPU Usage \n\n{}%".format(metrics)
        )

        if Configrations.CloseThreads:
          break

        time.sleep(1)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def UpdateAttendanceCount(self):
    try:
      while True:
        self.AttendanceCount.configure(
          text = "Attendance \n\n{}".format(len(DatabaseManager.Attendance))
        )

        if Configrations.CloseThreads:
          break

        time.sleep(5)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def Create(self, parent):
    try:
      parent.rowconfigure(0, weight = 1)
      parent.rowconfigure(1, weight = 3)
      parent.rowconfigure(2, weight = 1)

      parent.columnconfigure(0, weight = 1)
      parent.columnconfigure(1, weight = 3)
      parent.columnconfigure(2, weight = 1)

      ContentFrame = customtkinter.CTkFrame(parent)
      ContentFrame.grid(
        row = 1,
        column = 1,
        sticky = "new"
      )

      ContentFrame.rowconfigure(0, weight = 1)
      ContentFrame.rowconfigure(1, weight = 1)

      ContentFrame.columnconfigure(0, weight = 1)
      ContentFrame.columnconfigure(1, weight = 1)
      ContentFrame.columnconfigure(2, weight = 1)
      ContentFrame.columnconfigure(3, weight = 1)

      capture_button = customtkinter.CTkButton(
        ContentFrame,
        text = "Start Capture",
        command = self.StartCapturing,
        font=customtkinter.CTkFont(size=15)
      )
      capture_button.grid(
        row = 0,
        column = 0,
        columnspan = 2,
        sticky = "nswe"
      )

      StopCaptureButton = customtkinter.CTkButton(
        ContentFrame,
        text = "Stop Capture",
        command = self.StopCapturing,
        height = 50,
        fg_color = "red",
        font = customtkinter.CTkFont(size = 15)
      )
      StopCaptureButton.grid(
        row = 0,
        column = 2,
        columnspan = 2,
        sticky = "nswe"
      )

      CamerasStatusFrame = customtkinter.CTkFrame(ContentFrame, corner_radius = 0)
      CamerasStatusFrame.grid(
        row = 1,
        column = 0,
        sticky = "nsew"
      )
      CamerasStatusFrame.grid_propagate(False)

      self.CamerasStatusHeader = customtkinter.CTkLabel(
        CamerasStatusFrame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Camera Status"
      )
      self.CamerasStatusHeader.pack(
        padx = 5,
        pady = 10
      )
      self.CameraStatus = customtkinter.CTkLabel(CamerasStatusFrame)
      self.CameraStatus.pack()

      DatabaseStatusFrame = customtkinter.CTkFrame(
        ContentFrame,
        corner_radius = 0
      )
      DatabaseStatusFrame.grid(
        row = 1,
        column = 1,
        sticky = "nsew"
      )
      DatabaseStatusFrame.grid_propagate(False)

      self.DatabaseStatusHeader = customtkinter.CTkLabel(
        DatabaseStatusFrame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Database Status"
      )
      self.DatabaseStatusHeader.pack(
        padx = 5,
        pady = 10
      )


      self.DatabaseStatus = customtkinter.CTkLabel(DatabaseStatusFrame)
      self.DatabaseStatus.pack()

      AttendanceCountFrame = customtkinter.CTkFrame(
        ContentFrame,
        corner_radius = 0
      )
      AttendanceCountFrame.grid(
        row = 1,
        column = 2,
        sticky = "nsew"
      )
      AttendanceCountFrame.grid_propagate(False)

      self.AttendanceCount = customtkinter.CTkLabel(
        AttendanceCountFrame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Attendance \n\n0"
      )
      self.AttendanceCount.pack(
        padx = 5,
        pady = 15
      )
      CPUCountFrame = customtkinter.CTkFrame(
        ContentFrame,
        corner_radius = 0
      )
      CPUCountFrame.grid(
        row = 1,
        column = 3,
        sticky = "nsew"
      )
      CPUCountFrame.grid_propagate(False)

      self.CPUCount = customtkinter.CTkLabel(
        CPUCountFrame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "CPU Usage \n\n0"
      )
      self.CPUCount.pack(
        padx = 5,
        pady = 15
      )

      threading.Thread(target = self.UpdateCPUMetrics).start()
      threading.Thread(target = self.UpdateAttendanceCount).start()
      threading.Thread(target = self.UpdateDatabaseStatus).start()
      threading.Thread(target = self.UpdateCamerasStatus).start()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)  