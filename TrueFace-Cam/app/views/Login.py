import os
import sys
import customtkinter

from main import Main
from app.config.context import Context
from app.controllers.auth import login

class Login():
  def __init__(self):
    self._data_manager = Context()

  def check_user(self):
    result = login(
      self.email_entry.get(),
      self.password_entry.get()
    )

    if result:
      self._data_manager.set_token(result)
      self.window.destroy()
      Main().start_program()

  def lunch_view(self):
    try:
      self.window = customtkinter.CTk()
      self.window.geometry("400x170")
      self.window.iconbitmap("logo.ico")
      self.window.resizable(
        width = 0,
        height = 0
      )

      self.window.title("Login To TrueFace")

      content_frame = customtkinter.CTkFrame(self.window)
      content_frame.pack(
        padx = 20,
        pady = 20
      )

      email_label = customtkinter.CTkLabel(
        content_frame,
        text = "Email:"
      )
      email_label.grid(
        row = 0,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.email_entry = customtkinter.CTkEntry(
        content_frame,
        width = 250
      )
      self.email_entry.grid(
        row = 0,
        column = 1,
        padx = 10
      )

      password_label = customtkinter.CTkLabel(
        content_frame,
        text = "Password:"
      )
      password_label.grid(
        row = 1,
        column = 0,
        padx = 10,
      )

      self.password_entry = customtkinter.CTkEntry(
        content_frame,
        width = 250,
        show = "*"
      )
      self.password_entry.grid(
        row = 1,
        column = 1,
        padx = 10,
      )

      save_button = customtkinter.CTkButton(
        content_frame,
        text = "Login",
        command = self.check_user
      )
      save_button.grid(
        row = 6,
        columnspan = 2,
        padx = 10,
        pady = 10,
        sticky = "nsew",
      )

      self.window.mainloop()

    except Exception as e:
      ExceptionType, ExceptionObject, ExceptionTraceBack = sys.exc_info()
      fname = os.path.split(ExceptionTraceBack.tb_frame.f_code.co_filename)[1]
      print(ExceptionType, fname, ExceptionTraceBack.tb_lineno)
      print(ExceptionObject)