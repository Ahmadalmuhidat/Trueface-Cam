from django.urls import path
from .controllers import classes, students, attendance

urlpatterns = [
  # attendance
  path('get_current_class_attendance', attendance.get_current_class_attendance),
  path('search_attendance', attendance.search_attendance),
  path('check_attendance', attendance.check_attendance),
  path('insert_attendance', attendance.insert_attendance),
  path('get_class_attendance_report', attendance.get_class_attendance_report),

  # classes
  path('get_current_teacher_classes', classes.get_current_teacher_classes),

  # studnets
  path('get_class_students', students.get_class_students),
  path('get_students_with_face_encode', students.get_students_with_face_encode),
]
