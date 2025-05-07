import os
import sys
import requests
import json

from app.core.data_manager import Data_Manager
from CTkMessagebox import CTkMessagebox

def get_students_with_face_encode():
  try:
    database_manager = Data_Manager()
    data = {
      "current_class": database_manager.current_class,
    }
    response = requests.get(
      database_manager.config.get_base_url() + "/teacher/get_students_with_face_encode",
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

def get_current_class_students():
  try:
    database_manager = Data_Manager()
    data = {
      "current_class": database_manager.current_class
    }
    response = requests.get(
      database_manager.config.get_base_url() + "/teacher/get_class_students",
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