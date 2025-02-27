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