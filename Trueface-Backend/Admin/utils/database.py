from django.db import connection

class Database:
  @staticmethod
  def ExecuteGetQuery(query, data=None):
    try:
      with connection.cursor() as cursor:
        cursor.execute(query, data)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
      print("Database error:", str(e))
      return []

  @staticmethod
  def ExecutePostQuery(query, data=None):
    try:
      with connection.cursor() as cursor:
        cursor.execute(query, data)
      return True
    except Exception as e:
      print("Database error (POST):", str(e))
      return False