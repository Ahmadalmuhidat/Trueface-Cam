import sys
import os
import time
import cv2
import threading
import json

from CTkMessagebox import CTkMessagebox
from datetime import datetime
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
  
  def returnActivateCapturing(self):
    try:
      return CameraManager.ActivateCapturing

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def listWorkingCameras(self):
    try:
      TestCam = cv2.VideoCapture(0)

      if TestCam.isOpened():
        is_reading, img = TestCam.read()

        if is_reading:
          self.CameraActive = True
          title = "Camera Activated"
          message = "Camera has been tested successfully"
          icon = "check"
          CTkMessagebox(title=title, message=message, icon=icon)
        else:
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

  def CaptureAndAnalyze(self):
    try:
      cap = cv2.VideoCapture(0)

      while CameraManager.ActivateCapturing:
        ret, frame = cap.read()

        if ret:
          img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          self.FramesQueue.put(img_rgb)

          thread = threading.Thread(target=self.AnalyzeFace, args=(frame,))
          thread.start()

        time.sleep(0.1)
  
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
  
  def startCapturing(self):
    try:
      with open('configrations.json', 'r') as file:
          WorkingHour = json.load(file)['Working_Hours']
          WorkingHourStart = WorkingHour['start']
          WorkingHourEnd = WorkingHour['end']
          CurrentTime = datetime.now().strftime("%H:%M")

      # if not (WorkingHourStart <= CurrentTime < WorkingHourEnd):
      #     title = "Action Failed"
      #     message = "You can only scan between {} and {}, now it's {}".format(WorkingHourStart, WorkingHourEnd, CurrentTime)
      #     icon = "cancel"
      #     CTkMessagebox(title=title, message=message, icon=icon)
      #     return

      if not CameraManager.ActivateCapturing:
        if self.CameraActive:
          CameraManager.ActivateCapturing = True
          StopEvent = threading.Event()
          CaptureThread = threading.Thread(target=self.CaptureAndAnalyze)
          CameraManager.CaptureThreads.append(CaptureThread)
          CameraManager.CaptureEvents.append(StopEvent)
          CaptureThread.start()
        else:
          title = "Error"
          message = "Failed to find active cameras"
          icon = "cancel"
          CTkMessagebox(title=title, message=message, icon=icon)
      else:
        title = "Action Failed"
        message = "Camera is already capturing"
        icon = "cancel"
        CTkMessagebox(title=title, message=message, icon=icon)       

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def stopCapturing(self):
    try:
      if CameraManager.ActivateCapturing:
        self.closeLoadingScreen()
        
        CameraManager.ActivateCapturing = False
        CameraManager.CaptureEvents[0].set()
        CameraManager.CaptureThreads[0].join(timeout=5)
        CameraManager.CaptureThreads.clear()
        CameraManager.CaptureEvents.clear()
      else:
        title = "Action Failed"
        message = "Camera is not capturing"
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

  def showVideoFrame(self):
    try:
      threading.Thread(target=self.viewCam).start()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def closeLoadingScreen(self):
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