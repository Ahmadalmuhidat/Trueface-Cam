import os
import sys
import requests
import winsound
import json

from CTkMessagebox import CTkMessagebox
from app.core.data_manager import Data_Manager

def get_current_class_attendance():
  try:
    database_manager = Data_Manager()
    data = {
      "current_class": database_manager.get_current_class()
    }
    response = requests.get(
      database_manager.get_config().get_base_url() + "/teacher/get_current_class_attendance",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      database_manager.set_current_lecture_attendance(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while getting the attendance",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass

def search_attendance(student_id):
  try:
    database_manager = Data_Manager()
    data = {
      "student_id": student_id,
    }
    response = requests.get(
      database_manager.get_config().get_base_url() + "/teacher/search_attendance",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      database_manager.set_current_lecture_attendance(response.get("data"))
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while searching in the attendance",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass

def check_attendance(student_id):
  try:
    database_manager = Data_Manager()
    data = {
      "student_id": student_id,
      "current_class": database_manager.get_current_class()
    }
    response = requests.get(
      database_manager.get_config().get_base_url() + "/teacher/check_attendance",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      return response.get("data")
    else:
      title = "Error"
      message = response.get("error")
      icon = "cancel"
      CTkMessagebox(
        title = title,
        message = message if message else "Something went wrong while checking student attendance",
        icon = icon
      )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass

def insert_attendance(student_id, student_name):
  try:
    if not check_attendance(student_id):
      database_manager = Data_Manager()
      data = {
        "student_id": student_id,
        "current_class": database_manager.get_current_class()
      }
      response = requests.post(
        database_manager.get_config().get_base_url() + "/teacher/insert_attendance",
        data = data
      ).content
      response = json.loads(response.decode('utf-8'))

      if response.get("status_code") == 200:
        frequency = 2500
        duration = 500  # 1 second
        winsound.Beep(
          frequency,
          duration
        )
        CTkMessagebox(
          title = "Match Found",
          message = "{} has been signed".format(student_name),
          icon = "check"
        )
      else:
        title = "Error"
        message = response.get("error")
        icon = "cancel"
        CTkMessagebox(
          title = title,
          message = message if message else "Something went wrong while inserting attendance",
          icon = icon
        )

  except Exception as e:
    ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
    fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
    print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
    print(ExceptionObject)
    pass
