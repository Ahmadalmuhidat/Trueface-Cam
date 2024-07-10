import os
import sys
import cv2
import json

from DatabaseManager import DatabaseManager

class QRReader(DatabaseManager):
  def __init__(self) -> None:
    try:
      super().__init__()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass

  def ReadQRCode(self, image):
    try:
      qrcode = cv2.QRCodeDetector()
      result = qrcode.detectAndDecodeMulti(image)

      if len(result) == 4:
        retval, decoded_info, points, _ = result
      elif len(result) == 3:
        retval, decoded_info, points = result
      else:
        raise ValueError("Unexpected number of values returned")

      if points is not None:
          points = points.astype(int)
          for i in range(len(decoded_info)):
              points_array = points[i].reshape((-1, 1, 2))
              image = cv2.polylines(image, [points_array], True, (0, 255, 0), 2)
              info = json.loads(decoded_info[i])

              if info["Provider"] == "TimeWizeAI":
                self.InsertAttendance(info["StudentID"])
              else:
                pass

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
      pass
