import os
import sys
import cv2
import json

from app.config.context import Context
from app.controllers.attendance import insert_attendance

class QR_Reader_Module(Context):
  def read_qr_code(self, image):
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
          image = cv2.polylines(
            image,
            [points_array],
            True,
            (0, 255, 0),
            2
          )
          info = json.loads(decoded_info[i])

          if info["Provider"] == "TrueFace":
            insert_attendance(info["student_id"], info["student_name"])
            break

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)
      pass