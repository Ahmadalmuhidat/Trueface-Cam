import sys
import os
import customtkinter
import json
import threading

from DatabaseManager import DatabaseManager
from CTkMessagebox import CTkMessagebox

class Settings(DatabaseManager):
  def __init__(self):
    try:
      super().__init__()

      self.getSettings()
      self.getClasses()

      self.class_id_title_map = {f"{x[1]} {x[2]}-{x[3]}"  : x[0] for x in self.Classes}

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)
  

  def refreshSettings(self):
    try:
      # with open('configrations.json', 'r') as file:
      #   Settings = json.load(file)
      #   Settings['Database']['host'] = self.HostEntry.get()
      #   Settings['Database']['user'] = self.UserEntry.get()
      #   Settings['Database']['password'] = self.PasswordEntry.get()
      #   Settings['Database']['database'] = self.DatabaseEntry.get()
      #   Settings['Activation_Key'] = self.ActivationKeyEntry.get()

      # with open('configrations.json', 'w') as file:
      #   json.dump(Settings, file, indent=2)

      # self.getSettings()

      # self.HostEntry.configure(
      #   placeholder_text = self.Host
      # )
      # self.UserEntry.configure(
      #   placeholder_text = self.User
      # )
      # self.PasswordEntry.configure(
      #   placeholder_text = self.Password
      # )
      # self.DatabaseEntry.configure(
      #   placeholder_text = self.Database
      # )
      # self.ActivationKeyEntry.configure(
      #   placeholder_text = self.ActivationKey
      # )

      DatabaseManager.CurrentClass = self.class_id_title_map[self.CurrentLectureEntry.get()]

      # threading.Thread(target=self.connect).start()
      # threading.Thread(target=self.checkCustomerLicenseStatus).start()

      self.getStudents()
      self.getAttendance()

      CTkMessagebox(title="Info", message="Settings has been updated", icon="check")

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)

  def create(self, parent):
    try:
      ContentFrame = customtkinter.CTkFrame(parent)
      ContentFrame.pack(
        padx=20,
        pady=20
      )

      # Hostlabel = customtkinter.CTkLabel(
      #   ContentFrame,
      #   text="Host:"
      # )
      # Hostlabel.grid(row=0, column=0, padx=10, pady=10)
      # self.HostEntry = customtkinter.CTkEntry(
      #   ContentFrame,
      #   width=400
      # )
      # self.HostEntry.grid(
      #   row=0,
      #   column=1,
      #   padx=10,
      #   pady=10
      # )
      # self.HostEntry.insert(0, self.Host)

      # Userlabel = customtkinter.CTkLabel(
      #   ContentFrame,
      #   text="User:"
      # )
      # Userlabel.grid(
      #   row=1,
      #   column=0,
      #   padx=10,
      #   pady=10
      # )
      # self.UserEntry = customtkinter.CTkEntry(
      #   ContentFrame,
      #   width=400
      # )
      # self.UserEntry.grid(
      #   row=1,
      #   column=1,
      #   padx=10,
      #   pady=10
      # )
      # self.UserEntry.insert(0, self.User)

      # Passwordlabel = customtkinter.CTkLabel(
      #   ContentFrame,
      #   text="Password:"
      # )
      # Passwordlabel.grid(
      #   row=2,
      #   column=0,
      #   padx=10,
      #   pady=10
      # )
      # self.PasswordEntry = customtkinter.CTkEntry(
      #   ContentFrame,
      #   width=400
      # )
      # self.PasswordEntry.grid(
      #   row=2,
      #   column=1,
      #   padx=10,
      #   pady=10
      # )
      # self.PasswordEntry.insert(0, self.Password)

      # Databaselabel = customtkinter.CTkLabel(
      #   ContentFrame,
      #   text="Database:"
      # )
      # Databaselabel.grid(
      #   row=3,
      #   column=0,
      #   padx=10,
      #   pady=10
      # )
      # self.DatabaseEntry = customtkinter.CTkEntry(
      #   ContentFrame,
      #   width=400
      # )
      # self.DatabaseEntry.grid(
      #   row=3,
      #   column=1,
      #   padx=10,
      #   pady=10
      # )
      # self.DatabaseEntry.insert(0, self.Database)

      # ActivationKeylabel = customtkinter.CTkLabel(
      #   ContentFrame,
      #   text="Activation Key:"
      # )
      # ActivationKeylabel.grid(
      #   row=4,
      #   column=0,
      #   padx=10,
      #   pady=10
      # )
      # self.ActivationKeyEntry = customtkinter.CTkEntry(
      #   ContentFrame,
      #   width=400
      # )
      # self.ActivationKeyEntry.grid(
      #   row=4,
      #   column=1,
      #   padx=10,
      #   pady=10
      # )
      # self.ActivationKeyEntry.insert(0, self.ActivationKey)

      CurrentLecturelabel = customtkinter.CTkLabel(
        ContentFrame,
        text="Current Teacher:"
      )
      CurrentLecturelabel.grid(
        row=5,
        column=0,
        padx=10,
        pady=10
      )
      self.CurrentLectureEntry = customtkinter.CTkComboBox(
        ContentFrame,
        values=[f"{x[1]} {x[2]}-{x[3]}" for x in self.Classes],
        width=400
      )
      self.CurrentLectureEntry.grid(
        row=5,
        column=1,
        padx=10,
        pady=10
      )
      self.CurrentLectureEntry.set("None")

      save_button = customtkinter.CTkButton(ContentFrame)
      save_button.grid(
        row=6,
        columnspan=2,
        padx=10,
        pady=10,
        sticky="nsew",
      )
      save_button.configure(
        text="Refresh Settings",
        command=self.refreshSettings
      )

    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)
      print(exc_obj)