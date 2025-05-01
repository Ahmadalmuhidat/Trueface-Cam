import os
import sys
import cv2

class Camera:
  def __init__(self, index, name):
    self.name = name
    self.index = index
  
  def test(self):
    try:
      camera = cv2.VideoCapture(self.index)

      if camera.isOpened():
        is_reading, frame = camera.read()

        if is_reading:
          camera.release() 
          cv2.destroyAllWindows()
          return True
      return False

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass

  def view(self):
    try:
      cap = cv2.VideoCapture(self.index)
      WindowTitle = "Camera View"

      while True:
        is_reading, frame = cap.read()

        if is_reading:
          cv2.imshow(WindowTitle, frame)
          UserQuit = cv2.waitKey(1) & 0xFF == ord('q')
          UserClosedWindow = cv2.getWindowProperty(WindowTitle, cv2.WND_PROP_VISIBLE) < 1

          if UserQuit or UserClosedWindow: 
            break

      cap.release() 
      cv2.destroyAllWindows()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass