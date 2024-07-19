import os
import sys
import cv2
import threading

from CTkMessagebox import CTkMessagebox
from DatabaseManager import DatabaseManager
from cv2_enumerate_cameras import enumerate_cameras

class CameraManager(DatabaseManager):
  ActivateCapturing = False
  CaptureEvents = []
  CaptureThreads = []
  AvailableCameras = {}
  CurrentCamera = 0

  def __init__(self) -> None:
    try:
      super().__init__()

      self.CameraActive = False
      self.ScanningLoadingScreenRunning = False
      self.LoadingScreen = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def UpdateCurrentCamera(self, index):
    try:
      CameraManager.CurrentCamera = index

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def ReturnActivateCapturing(self):
    try:
      return CameraManager.ActivateCapturing

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def ListWorkingCameras(self):
    try:
      for CameraInfo in enumerate_cameras():
        CameraManager.AvailableCameras[CameraInfo.index] = CameraInfo.name

      TestCam = cv2.VideoCapture(CameraManager.CurrentCamera)

      if TestCam.isOpened():
        is_reading, img = TestCam.read()

        if is_reading:
          self.CameraActive = True
          title = "Camera Activated"
          message = "Camera has been tested successfully"
          icon = "check"
          CTkMessagebox(title=title, message=message, icon=icon)

      if not self.CameraActive:
        title = "Camera Not Activate"
        message = "Camera testing has failed"
        icon = "cancel"
        CTkMessagebox(title=title, message=message, icon=icon)

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def viewCam(self):
    if CameraManager.CurrentCamera:
      cap = cv2.VideoCapture(CameraManager.CurrentCamera)
      WindowTitle = "Camera View"

      while True:
        ret, frame = cap.read()

        if ret:
          cv2.imshow(WindowTitle, frame)
          UserQuit = cv2.waitKey(1) & 0xFF == ord('q')
          UserClosedWindow = cv2.getWindowProperty(
            WindowTitle, cv2.WND_PROP_VISIBLE
          ) < 1

          if UserQuit or UserClosedWindow: 
            break

      cap.release() 
      cv2.destroyAllWindows()
    else:
      title = "No Camera Selected"
      message = "Please select camera before testing"
      icon = "cancel"
      CTkMessagebox(title=title, message=message, icon=icon)

  def ShowVideoFrame(self):
    try:
      threading.Thread(target=self.viewCam).start()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def CloseLoadingScreen(self):
    try:
      if self.ScanningLoadingScreenRunning and self.LoadingScreen:
        self.ScanningLoadingScreenRunning = False
        self.LoadingScreen.destroy()
        self.LoadingScreen = None

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass