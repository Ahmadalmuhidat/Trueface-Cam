import sys
import os

class Configrations:
  window = None
  close_threads = False

  def __init__(self) -> None:
    self._base_url = "http://localhost:8000"

  @classmethod
  def set_close_threads(cls, close_threads):
    cls.close_threads = close_threads

  @classmethod
  def get_close_threads(cls):
    return cls.close_threads

  @classmethod
  def set_window(cls, window):
    cls.window = window

  @classmethod
  def get_window(cls):
    return cls.window

  def get_base_url(self):
    return self._base_url