from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..utils.database import Database

@csrf_exempt
def GetClasses(request):
  if request.method == "GET":
    try:
      query = '''
        SELECT
          Classes.*,
          Users.Name,
          Courses.Title
        FROM
          Classes
        LEFT JOIN
          Courses
        ON
          Courses.ID = Classes.Course
        LEFT JOIN
          Users
        ON
          Users.ID = Classes.Instructor
      '''
      data = Database.ExecuteGetQuery(query)
      return JsonResponse({
        "status_code": 200,
        "data": data
      })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def SearchClass(request):
  if request.method == "GET":
    try:
        class_id = request.GET.get('class_id')
        data = [class_id]
        query = '''
          SELECT
            Classes.*,
            Courses.Title
          FROM
            Classes
          LEFT JOIN
            Courses
          ON
            Courses.ID = Classes.Course
          WHERE
            Classes.ID = %s
        '''
        data = Database.ExecuteGetQuery(query, data)
        return JsonResponse({
          "status_code": 200,
          "data": data
        })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def RemoveClass(request):
  if request.method == "POST":
    try:
      
      class_id = request.POST.get('class_id')
      query = '''
        DELETE FROM
          Classes
        WHERE
          ID = %s
      '''
      if Database.ExecutePostQuery(query, [class_id]):
        query = '''
          DELETE FROM
            ClassStudentRelation
          WHERE
            Class = %s
        '''
        Database.ExecutePostQuery(query, [class_id])
      return JsonResponse({
        "status_code": 200,
        "data": True
      })
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def InsertClassStudentRelation(request):
  if request.method == "POST":
    try:
      print(request.POST.get('relation_id'))
      data = (
        request.POST.get('relation_id'),
        request.POST.get('student_id'),
        request.POST.get('class_id'),
        request.POST.get('day')
      )
      query = '''
        INSERT INTO
          ClassStudentRelation
          (
            ID,
            Student,
            Class,
            Day
          )
        VALUES
        (
          %s, 
          %s,
          %s,
          %s
        )
      '''
      Database.ExecutePostQuery(query, data)
      return JsonResponse({"status_code": 200,"data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def ClearClassStudentRelation(request):
  if request.method == "POST":
    try:
      student_id = request.POST.get('student_id')
      query = '''
        DELETE FROM
          ClassStudentRelation
        WHERE
          Student = %s
      '''
      Database.ExecutePostQuery(query, [student_id])
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def InsertClass(request):
  if request.method == "POST":
    try:
      data = (
        request.POST.get('class_id'),
        request.POST.get('subject'),
        request.POST.get('catalog_nbr'),
        request.POST.get('academic_career'),
        request.POST.get('course'),
        request.POST.get('offering_nbr'),
        request.POST.get('start_time'),
        request.POST.get('end_time'),
        request.POST.get('section'),
        request.POST.get('component'),
        request.POST.get('campus'),
        request.POST.get('instructor_id'),
        request.POST.get('instructor_type'),
      )
      query = '''
        INSERT INTO
        Classes
        (
          ID,
          SubjectArea,
          CatalogNbr,
          AcademicCareer,
          Course,
          OfferingNbr,
          StartTime,
          EndTime,
          Section,
          Component,
          Campus,
          Instructor,
          InstructorType
        )
        VALUES
        (
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s,
          %s
        )
      '''
      Database.ExecutePostQuery(query, data)
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def GetClassesStudentRelation(request):
  if request.method == "GET":
    try:
      student_id = request.GET.get('student_id')
      data = [student_id]
      query = '''
        SELECT
          ClassStudentRelation.ID AS Relation,
          Classes.ID AS Class,
          Classes.SubjectArea,
          Classes.StartTime,
          Classes.EndTime,
          ClassStudentRelation.Day
        FROM
          Classes
        JOIN
          ClassStudentRelation
        ON
          Classes.ID = ClassStudentRelation.Class
        WHERE
          ClassStudentRelation.Student = %s
      '''
      data = Database.ExecuteGetQuery(query, data)
      return JsonResponse({"status_code": 200,"data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def RemoveClassStudentRelation(request):
  if request.method == "POST":
    try:
      relation_id = request.POST.get('relation_id')
      print(relation_id)
      data = [relation_id]
      query = '''
        DELETE FROM
          ClassStudentRelation
        WHERE
          ID = %s
      '''
      Database.ExecutePostQuery(query, data)
      return JsonResponse({"status_code": 200, "data": True})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)

@csrf_exempt
def GetClassesForSelection(request):
  if request.method == "GET":
    try:
      query = '''
        SELECT
          ID,
          SubjectArea,
          StartTime,
          EndTime
        FROM
          Classes
      '''
      data = Database.ExecuteGetQuery(query)
      return JsonResponse({"status_code": 200,"data": data})
    except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
  return JsonResponse({
    "error": "Method not allowed"
  }, status=405)