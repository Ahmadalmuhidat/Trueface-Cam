import os
import sys
import requests
import json

from app.core.data_manager import DataManager
from CTkMessagebox import CTkMessagebox
from app.models.student import Student

def get_students_with_face_encode():
  try:
    data = {
      "current_class": DataManager.current_class,
    }
    response = requests.get(
      DataManager.config.get_base_url() + "/teacher/get_students_with_face_encode",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      DataManager.current_class_students = [
        Student(
          data['ID'],
          data['FirstName'],
          data['MiddleName'],
          data['LastName'],
          data['Gender'],
          data['FaceID'],
          data['Createdate'],
        ) for data in response.get("data")
      ]
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

# def get_classes_students():
#   try:
#     data = {
#       "current_class": DataManager.current_class
#     }
#     response = requests.get(
#       DataManager.config.get_base_url() + "/teacher/get_class_students",
#       params = data
#     ).content
#     response = json.loads(response.decode('utf-8'))

#     if response.get("status_code") == 200:
#       DataManager.current_lecture_students = [
#         Student(
#           data['ID'],
#           data['FirstName'],
#           data['MiddleName'],
#           data['LastName'],
#           data['Gender']
#         ) for data in response.get("data")
#       ]
#     else:
#       title = "Error"
#       message = response.get("error")
#       icon = "cancel"
#       CTkMessagebox(
#         title = title,
#         message = message if message else "Something went wrong while getting the students",
#         icon = icon
#       )

#   except Exception as e:
#     ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
#     fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
#     print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
#     print(ExceptionObject)
#     pass