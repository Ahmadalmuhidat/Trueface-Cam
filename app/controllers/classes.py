import os
import sys
import requests
import json

from CTkMessagebox import CTkMessagebox
from app.core.data_manager import DataManager
from app.models.class_ import Class

def get_current_teacher_classes():
  try:
    database_manager = DataManager()
    data = {
      "current_teacher": database_manager.token
    }
    response = requests.get(
      database_manager.config.get_base_url() + "/teacher/get_current_teacher_classes",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      database_manager.current_teacher_classes = [
        Class(
          data['ID'],
          data['SubjectArea'],
          data['StartTime'],
          data['EndTime']
        ) for data in response.get("data")
      ]
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the classes",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass