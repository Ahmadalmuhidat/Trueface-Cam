import os
import sys
import requests
import json

from CTkMessagebox import CTkMessagebox
from app.config.context import Context

def get_current_teacher_classes():
  try:
    database_manager = Context()
    data = {
      "current_teacher": database_manager.get_token()
    }
    response = requests.get(
      database_manager.get_config().get_base_url() + "/get_current_teacher_classes",
      params = data
    ).content
    response = json.loads(response.decode('utf-8'))

    if response.get("status_code") == 200:
      database_manager.set_current_teacher_classes(response.get("data"))
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