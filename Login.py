import os
import sys
import customtkinter

from UserInterface import UserInterface
from DatabaseManager import DatabaseManager

class Login(DatabaseManager):
  def __init__(self):
    try:
      super().__init__()

      self.GetSettings()

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def Login(self):
    result = self.CheckUser(
      self.EmailEntry.get(),
      self.PasswordEntry.get()
    )

    if result:
      DatabaseManager.token 
      self.window.destroy()
      UserInterface().StartTheProgram()

  def Create(self):
    try:
      self.window = customtkinter.CTk()
      self.window.geometry("400x350")
      self.window.resizable(
        width = 0,
        height = 0
      )

      self.window.title("Login To TimeWizeAI")

      ContentFrame = customtkinter.CTkFrame(self.window)
      ContentFrame.pack(
        padx = 20,
        pady = 20
      )

      Emaillabel = customtkinter.CTkLabel(
        ContentFrame,
        text = "Email:"
      )
      Emaillabel.grid(
        row = 0,
        column = 0,
        padx = 10,
        pady = 10
      )

      self.EmailEntry = customtkinter.CTkEntry(
        ContentFrame,
        width = 250
      )
      self.EmailEntry.grid(
        row = 0,
        column = 1,
        padx = 10
      )

      Passwordlabel = customtkinter.CTkLabel(
        ContentFrame,
        text = "Password:"
      )
      Passwordlabel.grid(
        row = 1,
        column = 0,
        padx = 10,
      )

      self.PasswordEntry = customtkinter.CTkEntry(
        ContentFrame,
        width = 250,
        show = "*"
      )
      self.PasswordEntry.grid(
        row = 1,
        column = 1,
        padx = 10,
      )

      save_button = customtkinter.CTkButton(
        ContentFrame,
        text = "Login",
        command = self.Login
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
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

if __name__ ==  "__main__":
  login = Login().Create()