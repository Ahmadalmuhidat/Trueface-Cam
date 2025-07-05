import app.config.configrations as Configrations

class Class:
  def __init__(
    self, class_id, subject_area, catalog_nbr = None, academic_career = None,
    course= None, offering_nbr = None, start_time = None, end_time = None, section = None,
    component = None, campus = None, instructor_id = None, instructor_type = None
  ):
    self.class_id = class_id
    self.subject_area = subject_area
    self.catalog_nbr = catalog_nbr
    self.academic_career = academic_career
    self.Course = course
    self.offering_nbr = offering_nbr
    self.start_time = start_time
    self.end_time = end_time
    self.section = section
    self.component = component
    self.campus = campus
    self.instructor_id = instructor_id
    self.instructor_type = instructor_type

    self.config  = Configrations.Configrations()
    self.students = []

  def get_class_id(self):
    return self.class_id

  def get_subject_area(self):
    return self.subject_area

  def get_catalog_nbr(self):
    return self.catalog_nbr

  def get_academic_career(self):
    return self.academic_career

  def get_course(self):
    return self.Course

  def get_offering_nbr(self):
    return self.offering_nbr

  def get_start_time(self):
    return self.start_time

  def get_end_time(self):
    return self.end_time

  def get_section(self):
    return self.section

  def get_component(self):
    return self.component

  def get_campus(self):
    return self.campus

  def get_instructor_id(self):
    return self.instructor_id

  def get_instructor_type(self):
    return self.instructor_type

  def get_config(self):
    return self.config

  def get_students(self):
    return self.students

class RelationClass(Class):
  def __init__(
    self, class_id, SubjectArea, CatalogNBR=None, AcademicCareer=None, Course=None,
    OfferingNBR=None, StartTime=None, EndTime=None, Section=None, Component=None,
    Campus=None, InstructorID=None, InstructorType=None, relation_id=None, day=None
  ):
    super().__init__(
      class_id, SubjectArea, CatalogNBR, AcademicCareer,
      Course, OfferingNBR, StartTime, EndTime, Section,
      Component, Campus, InstructorID, InstructorType
    )

    self.relation_id = relation_id
    self.day = day
  
  def get_relation_id(self):
    return self.relation_id

  def get_day(self):
    return self.day