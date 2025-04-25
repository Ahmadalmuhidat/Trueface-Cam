import os
import sys
import cv2
import time
import threading

from CTkMessagebox import CTkMessagebox
from app.core.data_manager import DataManager
from app.core.face_recognition_module import FaceRecognitionModule
from cv2_enumerate_cameras import enumerate_cameras
from app.models.camera import Camera

class CameraManagerModule():
  activate_capturing = False
  capture_events = []
  capture_threads = []
  available_cameras = []
  current_camera_index = 0

  def __init__(self) -> None:
    try:
      self.face_recognition_module = FaceRecognitionModule()

      self.camera_active = False
      self.ScanningLoadingScreenRunning = False
      self.LoadingScreen = None

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def set_current_camera(self, index):
    try:
      CameraManagerModule.current_camera_index = index

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def return_activate_capturing(self):
    try:
      return CameraManagerModule.activate_capturing

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def get_working_cameras(self):
    try:
      for camera in enumerate_cameras():
        new_camera = Camera(camera.index, camera.name)
        if new_camera.test():
          CameraManagerModule.available_cameras.append(new_camera)
          self.camera_active = True
          title = "Camera activated"
          message = "Camera has been tested successfully"
          icon = "check"
          CTkMessagebox(
            title = title,
            message = message,
            icon = icon
          )
        else:
          title = "Camera not activate"
          message = "Camera testing has failed"
          icon = "cancel"
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
      pass

  def view_current_camera_stream(self):
    try:
      if not CameraManagerModule.activate_capturing:
        if CameraManagerModule.current_camera_index:
          cam = CameraManagerModule.available_cameras[self.current_camera_index]
          cam.view()
        else:
          title = "No Camera Selected"
          message = "Please select camera before testing"
          icon = "cancel"
          CTkMessagebox(
            title = title,
            message = message,
            icon = icon
          )
      else:
          title = "Not Allowed"
          message = "Please make sure the camera is not already operating"
          icon = "cancel"
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
      if not DataManager.current_class:
        title = "Error"
        message = "Please select a lecture from the settings"
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message,
          icon = icon
        )
        return

      if not CameraManagerModule.activate_capturing:
        if self.camera_active:
          CameraManagerModule.activate_capturing = True

          StopEvent = threading.Event()
          CaptureThread = threading.Thread(target = self.capture_and_analyze)

          CameraManagerModule.capture_threads.append(CaptureThread)
          CameraManagerModule.capture_events.append(StopEvent)

          CaptureThread.start()
        else:
          title = "Error"
          message = "Failed to find active cameras"
          icon = "cancel"
          CTkMessagebox(
            title = title,
            message = message,
            icon = icon
          )
      else:
        title = "Action Failed"
        message = "Camera is already capturing"
        icon = "cancel"
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
      pass

  def stop_capturing(self):
    try:
      if CameraManagerModule.activate_capturing:
        self.close_loading_stream()

        CameraManagerModule.activate_capturing = False
        CameraManagerModule.capture_events[0].set()
        CameraManagerModule.capture_threads[0].join(timeout=5)
        CameraManagerModule.capture_threads.clear()
        CameraManagerModule.capture_events.clear()

      else:
        title = "Action Failed"
        message = "Camera is not capturing"
        icon = "cancel"
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
      pass

  def capture_and_analyze(self):
    try:
      cap = cv2.VideoCapture(CameraManagerModule.current_camera_index)

      while CameraManagerModule.activate_capturing:
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
      if self.ScanningLoadingScreenRunning and self.LoadingScreen:
        self.ScanningLoadingScreenRunning = False
        self.LoadingScreen.destroy()
        self.LoadingScreen = None

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass