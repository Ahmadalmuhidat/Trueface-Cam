import os
import sys
import customtkinter

from CTkMessagebox import CTkMessagebox
from app.core.camera_module import Camera_Manager_Module
from app.core.data_manager import Data_Manager
from app.controllers.classes import get_current_teacher_classes
from app.controllers.attendance import get_current_class_attendance
from app.controllers.students import get_students_with_face_encode

class Settings():
  def __init__(self):
    self.camera_manager = Camera_Manager_Module()
    self.data_manager = Data_Manager()

    get_current_teacher_classes()

    self.class_id_title_map = {
      f"{class_.get_subject_area()} {class_.get_start_time()}-{class_.get_end_time()}": class_.get_class_id() for class_ in self.data_manager.get_current_teacher_classes()
    }
    
    self.class_start_time_map = {
      f"{class_.get_subject_area()} {class_.get_start_time()}-{class_.get_end_time()}": class_.get_start_time() for class_ in self.data_manager.get_current_teacher_classes()
    }
    
    self.cameras_key_map = {
      camera.get_name(): camera.get_index() for camera in self.camera_manager.get_available_cameras()
    }
  
  def update_current_camera(self, choise):
    try:
      self.camera_manager.set_current_camera(self.cameras_key_map[choise])

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
  
  def update_settings(self):
    try:
      if not self.current_lecture_entry.get():
        title = "Missing Entries"
        message = "Please Select Current Lecture"
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message,
          icon = icon
        )
        return

      if not self.allowed_minutes_entry.get():
        title = "Missing Entries"
        message = "Please Enter Allowed Late Time"
        icon="cancel"
        CTkMessagebox(
          title = title,
          message = message,
          icon = icon
        )
        return

      self.data_manager.set_current_class(self.class_id_title_map[self.current_lecture_entry.get()])
      self.data_manager.set_start_time(self.class_start_time_map[self.current_lecture_entry.get()])
      self.data_manager.set_allowed_minutes(self.allowed_minutes_entry.get())

      get_students_with_face_encode()
      get_current_class_attendance()

      title = "Info"
      message = "Settings has been updated"
      icon = "check"
      CTkMessagebox(
        title = title,
        message = message,
        icon = icon
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def lunch_view(self, parent):
    try:
      content_frame = customtkinter.CTkFrame(parent)
      content_frame.pack(
        padx = 20,
        pady = 20
      )

      current_lecture_label = customtkinter.CTkLabel(
        content_frame,
        text = "Current Lecture:"
      )
      current_lecture_label.grid(
        row = 5,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.current_lecture_entry = customtkinter.CTkComboBox(
        content_frame,
        values = [f"{class_.get_subject_area()} {class_.get_start_time()}-{class_.get_end_time()}" for class_ in self.data_manager.get_current_teacher_classes()],
        width = 400
      )
      self.current_lecture_entry.grid(
        row = 5,
        column = 1,
        padx = 10,
        pady = 10
      )
      self.current_lecture_entry.set("none")

      allowed_minutes_label = customtkinter.CTkLabel(
        content_frame,
        text = "Allowed Minutes:"
      )
      allowed_minutes_label.grid(
        row = 6,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.allowed_minutes_entry = customtkinter.CTkEntry(
        content_frame,
        width = 400
      )
      self.allowed_minutes_entry.grid(
        row = 6,
        column = 1,
        padx = 10,
        pady = 10
      )

      available_cameras_label = customtkinter.CTkLabel(
        content_frame,
        text = "Available Cameras:"
      )
      available_cameras_label.grid(
        row = 7,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.available_cameras_entry = customtkinter.CTkComboBox(
        content_frame,
        values = list(self.cameras_key_map.keys()),
        width = 400,
        command = self.update_current_camera
      )
      self.available_cameras_entry.grid(
        row = 7,
        column = 1,
        padx = 10,
        pady = 10
      )
      self.available_cameras_entry.set(
        "none"
      )

      view_camera_button = customtkinter.CTkButton(
        content_frame,
        text = "Test Current Camera",
        command = self.camera_manager.view_current_camera_stream
      )
      view_camera_button.grid(
        row = 8,
        columnspan = 2,
        padx = 10,
        pady = 10,
        sticky = "nsew",
      )

      save_button = customtkinter.CTkButton(
        content_frame,
        text = "Update Settings",
        command = self.update_settings
      )
      save_button.grid(
        row = 9,
        columnspan = 2,
        padx = 10,
        pady = 10,
        sticky = "nsew",
      )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)