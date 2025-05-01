import os
import sys
import requests
import json

from CTkMessagebox import CTkMessagebox
from app.core.data_manager import DataManager

def get_report(start_time, allowed_minutes):
  try:
    data = {
      "start_time": start_time,
      "allowed_minutes": allowed_minutes,
      "current_classes": DataManager.current_class
    }
    response = requests.get(
      DataManager.config.get_base_url() + "/teacher/get_report",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      DataManager.current_lecture_attendance_report = response.get("data")
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the report",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass