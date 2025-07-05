import app.config.configrations as Configrations

class Course:
  def __init__(
    self, course_id, title, credit, maximum_units, long_course_title, offering_nbr,
    academic_group, subject_area, catalog_nbr, campus, academic_organization, component
  ):
    self.course_id = course_id
    self.title = title
    self.credit = credit
    self.maximum_units = maximum_units
    self.long_course_title = long_course_title
    self.offering_nbr = offering_nbr
    self.academic_group = academic_group
    self.subject_area = subject_area
    self.catalog_nbr = catalog_nbr
    self.campus = campus
    self.academic_organization = academic_organization
    self.component = component

    self.config  = Configrations.Configrations() 

  def get_course_id(self):
    return self.course_id

  def get_title(self):
    return self.title

  def get_credit(self):
    return self.credit

  def get_maximum_units(self):
    return self.maximum_units

  def get_long_course_title(self):
    return self.long_course_title

  def get_offering_nbr(self):
    return self.offering_nbr

  def get_academic_group(self):
    return self.academic_group

  def get_subject_area(self):
    return self.subject_area

  def get_catalog_nbr(self):
    return self.catalog_nbr

  def get_campus(self):
    return self.campus

  def get_academic_organization(self):
    return self.academic_organization

  def get_component(self):
    return self.component