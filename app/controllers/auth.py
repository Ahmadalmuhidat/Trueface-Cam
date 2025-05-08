import os
import sys
import requests
import json

from app.core.data_manager import Data_Manager
from CTkMessagebox import CTkMessagebox

def login(email, password):
  try:
    database_manager = Data_Manager()
    data = {
      "email": email,
      "password": password
    }
    response = requests.get(
      database_manager.get_config().get_base_url() + "/admin/check_user",
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
        message = message if message else "Something went wrong while checking user info",
        icon = icon
      )

  except Exception as e: 
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)