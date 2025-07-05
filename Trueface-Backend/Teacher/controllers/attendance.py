import uuid

from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def get_current_class_attendance(request):
  if request.method == "GET":
    current_class = request.GET.get("current_class")
    data = [current_class, date.today()]
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        TIME_FORMAT(Attendance.Time, '%%H:%%i') AS Time
      FROM
        Attendance
      LEFT JOIN
        Students
      ON
        Attendance.Student = Students.ID
      WHERE
        Attendance.Class = %s AND Attendance.Date = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def search_attendance(request):
  if request.method == "GET":
    attendance_id = request.GET.get("attendance_id")
    data = (attendance_id, date.today())
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        Attendance.Time
      FROM
        Attendance
      LEFT JOIN
        Students
      ON
        Attendance.Student = Students.ID
      WHERE
        Attendance.Student = %s
      AND
        Attendance.Date = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def check_attendance(request):
  if request.method == "GET":
    student_id = request.GET.get("student_id")
    current_class = request.GET.get("current_class")
    data = (date.today(), student_id, current_class)
    query = '''
      SELECT
        *
      FROM
        Attendance
      WHERE
        Date = %s
      AND
        Student = %s
      AND
        Class = %s
    '''
    is_present = len(Database.ExecuteGetQuery(query, data)) > 0
    return JsonResponse({"status_code": 200, "data": is_present})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def insert_attendance(request):
  if request.method == "POST":
    student_id = request.POST.get("student_id")
    current_class = request.POST.get("current_class")
    now = datetime.now()
    AttendanceID = str(uuid.uuid4())
    date_ = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    data = (AttendanceID, student_id, current_class, time, date_)
    query = '''
      INSERT INTO
        Attendance
      VALUES
      (
        %s,
        %s,
        %s,
        %s,
        %s
      )
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })

@csrf_exempt
def get_class_attendance_report(request):
  if request.method == "GET":
    start_time = request.GET.get("start_time")
    allowed_minutes = int(request.GET.get("allowed_minutes")) * 60
    current_class = request.GET.get("current_class")
    data = (start_time, allowed_minutes, current_class, date.today())
    query = '''
      SELECT
        Students.ID,
        Students.FirstName,
        Students.MiddleName,
        Students.LastName,
        CASE
          WHEN
            Attendance.Time IS NULL THEN 'absent'
          ELSE
            TIME_FORMAT(Attendance.Time, '%%H:%%i')
        END AS Time,
        CASE
          WHEN
            Attendance.Time IS NULL THEN FALSE
          WHEN
            TIME_TO_SEC(TIMEDIFF(Attendance.Time, %s)) > %s THEN 'late'
          ELSE
            'not late'
        END AS Lateness
      FROM
        Students
      LEFT JOIN
        Attendance
      ON
        Attendance.Student = Students.ID
      AND
        Attendance.Class = %s
      AND
        Attendance.Date = %s
    '''
    return JsonResponse({"status_code": 200, "data": Database.ExecuteGetQuery(query, data)})
  return JsonResponse({
    "status_code": 405,
    "error": "Method not allowed"
  })
