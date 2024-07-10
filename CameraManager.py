import os
import sys
import cv2
import threading

from CTkMessagebox import CTkMessagebox
from DatabaseManager import DatabaseManager

class CameraManager(DatabaseManager):
  ActivateCapturing = False
  CaptureEvents = []
  CaptureThreads = []

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
      for x in range(0, 10):
        TestCam = cv2.VideoCapture(x)

        if TestCam.isOpened():
          is_reading, img = TestCam.read()

          if is_reading:
            self.CameraActive = True
            title = "Camera Activated"
            message = "Camera has been tested successfully"
            icon = "check"
            CTkMessagebox(title=title, message=message, icon=icon)
            break

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
    cap = cv2.VideoCapture(0)
    WindowTitle = "Camera View"

    while True:
      ret, frame = cap.read()

      if ret:
        cv2.imshow(WindowTitle, frame) 

        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty(WindowTitle, cv2.WND_PROP_VISIBLE) < 1: 
          break

    cap.release() 
    cv2.destroyAllWindows()

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