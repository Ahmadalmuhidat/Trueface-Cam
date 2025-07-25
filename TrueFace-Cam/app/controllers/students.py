import os
import sys
import requests
import json

from app.config.context import Context
from CTkMessagebox import CTkMessagebox

def get_students_with_face_encode():
  try:
    data_manager = Context()
    data = {
      "current_class": data_manager.get_current_class(),
    }
    response = requests.get(
      data_manager.get_config().get_base_url() + "/get_students_with_face_encode",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      data_manager.set_current_class_students(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the students",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass

# remove this route and keep only one
def get_current_class_students():
  try:
    database_manager = Context()
    data = {
      "current_class": database_manager.get_current_class()
    }
    response = requests.get(
      database_manager.get_config().get_base_url() + "/get_class_students",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      database_manager.set_current_class_students(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the students",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass