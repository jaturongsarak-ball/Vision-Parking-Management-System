import pymysql

host = 'localhost'
user = 'root'
password = ''
database = 'vpms'

import pymysql

def execute_query(query, params=None):
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        
        connection.commit()
        connection.close()
        return cursor.rowcount
    
# def execute_query(query, params=None):
#     connection = pymysql.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=database,
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute(query, params)
            
#             # คำสั่ง SELECT คืนค่าแถวข้อมูล
#             if query.strip().upper().startswith("SELECT"):
#                 return cursor.fetchall()

#             # คำสั่ง INSERT, UPDATE, DELETE คืนค่าจำนวนแถวที่ได้รับผลกระทบ
#             connection.commit()
#             return cursor.rowcount
#     finally:
#         connection.close()