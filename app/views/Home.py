import os
import sys
import customtkinter
import psutil
import time
import requests
import threading
import json

from app.config.configrations import Configrations
from app.core.data_manager import Data_Manager
from app.core.camera_module import Camera_Manager_Module

class Home():
  def __init__(self):
    self._camera_manager = Camera_Manager_Module()
    self._data_manager = Data_Manager()
    self._config = Configrations()

  def update_camera_status(self):
    try:
      if self._camera_manager.found_active_connected_camera:
        self.camera_status.configure(
          text = "Connected",
          text_color = "green"
        )
      else:
        self.camera_status.configure(
          text= "Disconnected",
          text_color = "red"
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def update_database_status(self):
    try:
      response = requests.get(self._config.get_base_url() + "/",).content
      response_str = response.decode('utf-8')
      APIActive = json.loads(response_str)

      if not APIActive:
        self.database_status.configure(
          text = "Disconnected",
          text_color = "red"
        )
      else:
        self.database_status.configure(
          text = "Connected",
          text_color = "green"
        )   

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass 

  def update_cpu_metrics(self):
    try:
      while True:
        metrics = psutil.cpu_percent(interval=1)
        self.cpu_count.configure(
          text = "CPU Usage \n\n{}%".format(metrics)
        )

        if Configrations.close_threads:
          break

        time.sleep(1)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def update_attendance_count(self):
    try:
      while True:
        self.attendance_count.configure(
          text = "Attendance \n\n{}".format(len(self._data_manager.get_current_lecture_attendance()))
        )

        if Configrations.close_threads:
          break

        time.sleep(5)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def lunch_view(self, parent):
    try:
      parent.rowconfigure(0, weight = 1)
      parent.rowconfigure(1, weight = 3)
      parent.rowconfigure(2, weight = 1)

      parent.columnconfigure(0, weight = 1)
      parent.columnconfigure(1, weight = 3)
      parent.columnconfigure(2, weight = 1)

      content_frame = customtkinter.CTkFrame(parent)
      content_frame.grid(
        row = 1,
        column = 1,
        sticky = "new"
      )

      content_frame.rowconfigure(0, weight = 1)
      content_frame.rowconfigure(1, weight = 1)

      content_frame.columnconfigure(0, weight = 1)
      content_frame.columnconfigure(1, weight = 1)
      content_frame.columnconfigure(2, weight = 1)
      content_frame.columnconfigure(3, weight = 1)

      capture_button = customtkinter.CTkButton(
        content_frame,
        text = "Start Capture",
        command = self._camera_manager.start_capturing,
        font=customtkinter.CTkFont(size=15)
      )
      capture_button.grid(
        row = 0,
        column = 0,
        columnspan = 2,
        sticky = "nswe"
      )

      stop_capture_button = customtkinter.CTkButton(
        content_frame,
        text = "Stop Capture",
        command = self._camera_manager.stop_capturing,
        height = 50,
        fg_color = "red",
        font = customtkinter.CTkFont(size = 15)
      )
      stop_capture_button.grid(
        row = 0,
        column = 2,
        columnspan = 2,
        sticky = "nswe"
      )

      camera_status_frame = customtkinter.CTkFrame(content_frame, corner_radius = 0)
      camera_status_frame.grid(
        row = 1,
        column = 0,
        sticky = "nsew"
      )
      camera_status_frame.grid_propagate(False)

      self.camera_status_header = customtkinter.CTkLabel(
        camera_status_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Camera Status"
      )
      self.camera_status_header.pack(
        padx = 5,
        pady = 10
      )
      self.camera_status = customtkinter.CTkLabel(camera_status_frame)
      self.camera_status.pack()

      database_status_frame = customtkinter.CTkFrame(
        content_frame,
        corner_radius = 0
      )
      database_status_frame.grid(
        row = 1,
        column = 1,
        sticky = "nsew"
      )
      database_status_frame.grid_propagate(False)

      self.database_status_header = customtkinter.CTkLabel(
        database_status_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Database Status"
      )
      self.database_status_header.pack(
        padx = 5,
        pady = 10
      )

      self.database_status = customtkinter.CTkLabel(database_status_frame)
      self.database_status.pack()

      attendance_count_frame = customtkinter.CTkFrame(
        content_frame,
        corner_radius = 0
      )
      attendance_count_frame.grid(
        row = 1,
        column = 2,
        sticky = "nsew"
      )
      attendance_count_frame.grid_propagate(False)

      self.attendance_count = customtkinter.CTkLabel(
        attendance_count_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "Attendance \n\n0"
      )
      self.attendance_count.pack(
        padx = 5,
        pady = 15
      )
      cpu_count_frame = customtkinter.CTkFrame(
        content_frame,
        corner_radius = 0
      )
      cpu_count_frame.grid(
        row = 1,
        column = 3,
        sticky = "nsew"
      )
      cpu_count_frame.grid_propagate(False)

      self.cpu_count = customtkinter.CTkLabel(
        cpu_count_frame,
        bg_color = "transparent",
        font = customtkinter.CTkFont(size = 15),
        text = "CPU Usage \n\n0"
      )
      self.cpu_count.pack(
        padx = 5,
        pady = 15
      )

      # threading.Thread(target = self.update_cpu_metrics).start()
      # threading.Thread(target = self.update_attendance_count).start()
      # threading.Thread(target = self.update_database_status).start()
      # threading.Thread(target = self.update_camera_status).start()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)  