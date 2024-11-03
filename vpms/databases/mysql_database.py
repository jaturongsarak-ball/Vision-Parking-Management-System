import pymysql
from pymysql.cursors import DictCursor
from vpms.config import Database


class MySQL_Database:

    def __init__(self):
        self.connection = None
        self.host = Database.DB_HOST
        self.user = Database.DB_USER
        self.password = Database.DB_PASSWORD
        self.database = Database.DB_NAME
        self.cursorclass = DictCursor

    def connect(self):
        """สร้างการเชื่อมต่อฐานข้อมูล"""
        if self.connection is None:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=self.cursorclass
            )

    def close(self):
        """ปิดการเชื่อมต่อฐานข้อมูลหากมีการเชื่อมต่ออยู่"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def commit(self):
        """บันทึกการเปลี่ยนแปลงในฐานข้อมูล"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """ยกเลิกการเปลี่ยนแปลงในฐานข้อมูล"""
        if self.connection:
            self.connection.rollback()

    def cursor(self):
        """สร้างและส่งคืน cursor สำหรับดำเนินการกับฐานข้อมูล"""
        if self.connection:
            return self.connection.cursor()

    def select_fetchone(self, sql, params=None):
        """
        ดึงข้อมูลจากฐานข้อมูลตามคำสั่ง SQL และพารามิเตอร์ที่กำหนด
        :param sql: คำสั่ง SQL สำหรับดึงข้อมูล
        :param params: พารามิเตอร์สำหรับใช้กับคำสั่ง SQL (ถ้ามี)
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchone()
        self.close()
        if results:
            return results
        else:
            return None

    def select_fetchall(self, sql, params=None):
        """
        ดึงข้อมูลทั้งหมดจากฐานข้อมูลตามคำสั่ง SQL และพารามิเตอร์ที่กำหนด
        :param sql: คำสั่ง SQL สำหรับดึงข้อมูล
        :param params: พารามิเตอร์สำหรับใช้กับคำสั่ง SQL (ถ้ามี)
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        results = cursor.fetchall()
        self.close()
        if results:
            return results
        else:
            return None

    def insert(self, sql, params):
        """
        เพิ่มข้อมูลใหม่ลงในฐานข้อมูลตามคำสั่ง SQL และพารามิเตอร์ที่กำหนด
        :param sql: คำสั่ง SQL สำหรับการเพิ่มข้อมูล
        :param params: พารามิเตอร์สำหรับใช้กับคำสั่ง SQL
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.commit()
        self.close()