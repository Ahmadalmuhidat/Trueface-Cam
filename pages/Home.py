import customtkinter
import sys
import os
import psutil
import time
import threading

from FaceRecognitionModal import FaceRecognitionModal

class Home(FaceRecognitionModal):
  def __init__(self):
    try:
      super().__init__()

      self.CamsLabels = []
      self.ImagePath = None

      self.connect()
      self.checkCustomerLicenseStatus()
      self.listWorkingCameras()
      self.getIndividuals()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def updateCamerasStatus(self):
    try:
      if self.CameraActive:
        self.camera_status.configure(text="Connected", text_color="green")
      else:
        self.camera_status.configure(text="Disconnected", text_color="red")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def updateDatabaseStatus(self):
    try:
      if self.returnCursor():
        self.database_status.configure(text="Connected", text_color="green")
      else:
        self.database_status.configure(text="Disconnected", text_color="red")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass 

  def updateCPUMetrics(self):
    try:
      while True:
        metrics = psutil.cpu_percent(interval=1)
        self.CPU_count.configure(text="CPU Usage \n\n{}%".format(metrics))

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def updateAttendanceCount(self):
    try:
      while True:
        self.getAttendance()
        self.attendance_count.configure(text="Attendance \n\n{}".format(len(self.Attendance)))
        time.sleep(5)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def create(self, parent):
    try:
      parent.rowconfigure(0, weight=1)
      parent.rowconfigure(1, weight=3)
      parent.rowconfigure(2, weight=1)

      parent.columnconfigure(0, weight=1)
      parent.columnconfigure(1, weight=3)
      parent.columnconfigure(2, weight=1)

      content_frame = customtkinter.CTkFrame(parent)
      content_frame.grid(row=1, column=1, sticky="new")
      content_frame.rowconfigure(0, weight=1)
      content_frame.rowconfigure(1, weight=1)
      content_frame.columnconfigure(0, weight=1)
      content_frame.columnconfigure(1, weight=1)
      content_frame.columnconfigure(2, weight=1)
      content_frame.columnconfigure(3, weight=1)

      capture_button = customtkinter.CTkButton(content_frame, font=customtkinter.CTkFont(size=15))
      capture_button.grid(row=0, column=0, columnspan=2, sticky="nswe")
      capture_button.configure(text="Start Capture", command=self.startCapturing)

      StopCaptureButton = customtkinter.CTkButton(content_frame, font=customtkinter.CTkFont(size=15))
      StopCaptureButton.grid(row=0, column=2, columnspan=2, sticky="nswe")
      StopCaptureButton.configure(text="Stop Capture", command=self.stopCapturing, height=50, fg_color="red")

      cameras_status_frame = customtkinter.CTkFrame(content_frame, corner_radius=0)
      cameras_status_frame.grid(row=1, column=0, sticky="nsew")
      cameras_status_frame.grid_propagate(False)
      self.cameras_status_header = customtkinter.CTkLabel(cameras_status_frame, text="Camera Status")
      self.camera_status = customtkinter.CTkLabel(cameras_status_frame)
      self.cameras_status_header.pack(padx=5, pady=10)
      self.camera_status.pack()
      self.cameras_status_header.configure(bg_color="transparent", font=customtkinter.CTkFont(size=15))

      database_status_frame = customtkinter.CTkFrame(content_frame, corner_radius=0)
      database_status_frame.grid(row=1, column=1, sticky="nsew")
      database_status_frame.grid_propagate(False)
      self.database_status_header = customtkinter.CTkLabel(database_status_frame, text="Database Status")
      self.database_status = customtkinter.CTkLabel(database_status_frame)
      self.database_status_header.pack(padx=5, pady=10)
      self.database_status.pack()
      self.database_status_header.configure(bg_color="transparent", font=customtkinter.CTkFont(size=15))

      attendance_count_frame = customtkinter.CTkFrame(content_frame, corner_radius=0)
      attendance_count_frame.grid(row=1, column=2, sticky="nsew")
      attendance_count_frame.grid_propagate(False)
      self.attendance_count = customtkinter.CTkLabel(attendance_count_frame, text="Attendance \n\n0")
      self.attendance_count.pack(padx=5, pady=15)
      self.attendance_count.configure(bg_color="transparent", font=customtkinter.CTkFont(size=15))

      CPU_count_frame = customtkinter.CTkFrame(content_frame, corner_radius=0)
      CPU_count_frame.grid(row=1, column=3, sticky="nsew")
      CPU_count_frame.grid_propagate(False)
      self.CPU_count = customtkinter.CTkLabel(CPU_count_frame, text="CPU Usage \n\n0")
      self.CPU_count.pack(padx=5, pady=15)
      self.CPU_count.configure(bg_color="transparent", font=customtkinter.CTkFont(size=15))

      threading.Thread(target=self.updateCPUMetrics).start()
      # threading.Thread(target=self.updateAttendanceCount).start()
      threading.Thread(target=self.updateDatabaseStatus).start()
      threading.Thread(target=self.updateCamerasStatus).start()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)