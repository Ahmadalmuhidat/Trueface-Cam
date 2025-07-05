import app.config.configrations as Configrations

class User:
  def __init__(self, user_id, name, email, role):
    self.user_id = user_id
    self.name = name
    self.email = email
    self.role = role

    self.config = Configrations.Configrations()

  def get_user_id(self):
    return self.user_id

  def get_name(self):
    return self.name

  def get_email(self):
    return self.email

  def get_role(self):
    return self.role

  def get_config(self):
    return self.config