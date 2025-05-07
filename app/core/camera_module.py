import os
import sys
import cv2
import time
import threading

from CTkMessagebox import CTkMessagebox
from cv2_enumerate_cameras import enumerate_cameras
from app.core.data_manager import DataManager
from app.core.face_recognition_module import FaceRecognitionModule
from app.models.camera import Camera

class CameraManagerModule:
  activate_capturing = False
  found_active_connected_camera = False

  capture_events = []
  capture_threads = []
  available_cameras = []
  current_camera_index = 0

  def __init__(self) -> None:
    try:
      self.data_manager = DataManager()
      self.face_recognition_module = FaceRecognitionModule()

      self.scanning_loading_screen_running = False
      self.LoadingScreen = None

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  @classmethod
  def set_current_camera(cls, index):
    try:
      cls.current_camera_index = index

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  @classmethod
  def return_activate_capturing(cls):
    try:
      return cls.activate_capturing

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  @classmethod
  def get_working_cameras(cls):
    try:
      for camera in enumerate_cameras():
        new_camera = Camera(camera.index, camera.name)
        if new_camera.test():
          cls.available_cameras.append(new_camera)
          cls.found_active_connected_camera = True
          CTkMessagebox(
            title = "Camera activated",
            message = "Camera has been tested successfully",
            icon = "check"
          )
        else:
          CTkMessagebox(
            title = "Camera not activate",
            message = "Camera testing has failed",
            icon = "cancel"
          )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  @classmethod
  def view_current_camera_stream(cls):
    try:
      if not cls.activate_capturing:
        if cls.current_camera_index:
          cam = next((camera for camera in cls.available_cameras if camera.index == cls.current_camera_index), None)
          cam.view()
        else:
          CTkMessagebox(
            title = "No Camera Selected",
            message = "Please select camera before testing",
            icon = "cancel"
          )
      else:
          CTkMessagebox(
            title = "Not Allowed",
            message = "Please make sure the camera is not already operating",
            icon = "cancel"
          )

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def show_video_frame(self):
    try:
      threading.Thread(target=self.view_current_camera_stream).start()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)

  def start_capturing(self):
    try:
      if not self.data_manager.current_class:
        CTkMessagebox(
          title = "Error",
          message = "Please select a lecture from the settings",
          icon = "cancel"
        )
        return

      if not self.__class__.activate_capturing:
        if self.__class__.found_active_connected_camera:
          self.__class__.activate_capturing = True

          StopEvent = threading.Event()
          CaptureThread = threading.Thread(target = self.capture_and_analyze)

          self.__class__.capture_threads.append(CaptureThread)
          self.__class__.capture_events.append(StopEvent)

          CaptureThread.start()
        else:
          CTkMessagebox(
            title = "Error",
            message = "Failed to find active cameras",
            icon = "cancel"
          )
      else:
        CTkMessagebox(
          title = "Action Failed",
          message = "Camera is already capturing",
          icon = "cancel"
        )
    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def stop_capturing(self):
    try:
      if self.__class__.activate_capturing:
        self.close_loading_stream()

        self.__class__.activate_capturing = False
        self.__class__.capture_events[0].set()
        self.__class__.capture_threads[0].join(timeout=5)
        self.__class__.capture_threads.clear()
        self.__class__.capture_events.clear()

      else:
        CTkMessagebox(
          title = "Action Failed",
          message = "Camera is not capturing",
          icon = "cancel"
        )
    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def capture_and_analyze(self):
    try:
      cap = cv2.VideoCapture(self.__class__.current_camera_index)

      while self.__class__.activate_capturing:
        ret, frame = cap.read()

        if ret:
          img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          self.FramesQueue.put(img_rgb)
                
          FR_thread = threading.Thread(
            target = self.face_recognition_module.analyze_face,
            args = (frame,)
          )
          FR_thread.start()

          # QR_thread = threading.Thread(
          # 	target = self.ReadQRCode,
          # 	args = (frame,)
          # )
          # QR_thread.start()

        time.sleep(0.1)

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def close_loading_stream(self):
    try:
      if self.scanning_loading_screen_running and self.LoadingScreen:
        self.scanning_loading_screen_running = False
        self.LoadingScreen.destroy()
        self.LoadingScreen = None

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass