import os
import sys
import cv2
import time
import threading

from CTkMessagebox import CTkMessagebox
from cv2_enumerate_cameras import enumerate_cameras
from app.core.data_manager import Data_Manager
from app.core.face_recognition_module import Face_Recognition_Module
from app.models.camera import Camera

class Camera_Manager_Module:
  # static
  _instance = None
  _initialized = False

  def __new__(cls):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
    return cls._instance

  def __init__(self) -> None:
    # prevent re-initialization
    if self.__class__._initialized:
      return
    self.__class__._initialized = True

    # private
    self._data_manager = Data_Manager()
    self._face_recognition_module = Face_Recognition_Module()
    self._activate_capturing = False
    self._capture_events = []
    self._capture_threads = []
    self._available_cameras = []
    self._current_camera_index = 0

    # public
    self.found_active_connected_camera = False
    self.scanning_loading_screen_running = False
    self.loading_screen = None

  def set_current_camera(self, index):
    self._current_camera_index = index

  def get_current_camera(self):
    return self._current_camera_index

  def set_activate_capturing(self, activate_capturing):
    self._activate_capturing = activate_capturing

  def get_activate_capturing(self):
    return self._activate_capturing

  def get_working_cameras(self):
    try:
      for camera in enumerate_cameras():
        new_camera = Camera(camera.index, camera.name)
        if new_camera.test():
          self._available_cameras.append(new_camera)
          self.found_active_connected_camera = True
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

  def view_current_camera_stream(self):
    try:
      if not self._activate_capturing:
        if self._current_camera_index:
          cam = next((camera for camera in self._available_cameras if camera.get_index() == self._current_camera_index), None)
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

  def get_available_cameras(self):
    return self._available_cameras

  def show_video_frame(self):
    threading.Thread(target=self.view_current_camera_stream).start()

  def start_capturing(self):
    try:
      if not self._data_manager.get_current_class():
        CTkMessagebox(
          title = "Error",
          message = "Please select a lecture from the settings",
          icon = "cancel"
        )
        return

      if not self._activate_capturing:
        if self.found_active_connected_camera:
          self._activate_capturing = True

          StopEvent = threading.Event()
          CaptureThread = threading.Thread(target = self.capture_and_analyze)

          self._capture_threads.append(CaptureThread)
          self._capture_events.append(StopEvent)

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
      if self._activate_capturing:
        self.close_loading_stream()

        self._activate_capturing = False
        self._capture_events[0].set()
        self._capture_threads[0].join(timeout=5)
        self._capture_threads.clear()
        self._capture_events.clear()

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
      cap = cv2.VideoCapture(self._current_camera_index)

      while self._activate_capturing:
        ret, frame = cap.read()

        if ret:
          img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          self._face_recognition_module._frames_queue.put(img_rgb)
                
          FR_thread = threading.Thread(
            target = self._face_recognition_module.analyze_face,
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
      if self.scanning_loading_screen_running and self.loading_screen:
        self.scanning_loading_screen_running = False
        self.loading_screen.destroy()
        self.loading_screen = None

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass