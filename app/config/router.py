import customtkinter

from app.config.configrations import Configrations

class Router:
  def __init__(self):
    self.current_page = None
    self.config = Configrations()

  def clear_window(self):
    if self.current_page:
      self.current_page.pack_forget()

  def navigate(self, view_class):
    self.clear_window()

    self.config.window.configure(cursor="watch")
    self.config.window.update()

    frame = customtkinter.CTkFrame(self.config.window)
    view_instance = view_class()

    self.config.window.configure(cursor="")
    self.config.window.update()

    view_instance.lunch_view(frame)

    self.current_page = frame
    self.current_page.pack(fill="both", expand=True)