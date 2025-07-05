import base64

from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def get_class_students(request):
  if request.method == "GET":
    current_class = request.GET.get("current_class")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = days[date.today().weekday()]
    data = (current_class, today)
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        Students.Gender
      FROM
        Students
      JOIN
        ClassStudentRelation
      ON
        ClassStudentRelation.Student = Students.ID
      WHERE
        ClassStudentRelation.Class = %s
      AND
        ClassStudentRelation.Day = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def get_students_with_face_encode(request):
  if request.method == "GET":
    current_class = request.GET.get("current_class")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = days[date.today().weekday()]
    data = (current_class, today)
    query = '''
      SELECT
        Students.*
      FROM
        Students
      JOIN
        ClassStudentRelation
      ON
        ClassStudentRelation.Student = Students.ID
      WHERE
        ClassStudentRelation.Class = %s
      AND
        ClassStudentRelation.Day = %s
    '''
    rows = Database.ExecuteGetQuery(query, data)
    for row in rows:
      for key, value in row.items():
        if isinstance(value, bytes):
          row[key] = base64.b64encode(value).decode('utf-8')

    return JsonResponse({"status_code": 200, "data": rows})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
