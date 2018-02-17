import pymysql
import datetime
from cfenv import AppEnv

class DBHelper:

  def __init__(self, app_env):
    self.db_hostname = app_env.get_credential("hostname")
    self.db_port = int(app_env.get_credential("port"))
    self.db_username = app_env.get_credential("username")
    self.db_password = app_env.get_credential("password")
    self.db_name = app_env.get_credential("name")

  def connect(self):
    connection = pymysql.connect(host=self.db_hostname,
                                 port=self.db_port,
                                 user=self.db_username,
                                 password=self.db_password,
                                 db=self.db_name)
    return connection

  def create_table(self):
    connection = self.connect();
    try:
      with connection.cursor() as cursor:
        sql = """CREATE TABLE IF NOT EXISTS crimes (
                 id           INT NOT NULL AUTO_INCREMENT,
                 latitude     FLOAT(10,6),
                 longitude    FLOAT(10,6),
                 date         DATETIME,
                 category     VARCHAR(50),
                 description  VARCHAR(1000),
                 updated_at   TIMESTAMP,
                 PRIMARY KEY (id))"""
        cursor.execute(sql)
        connection.commit()
    finally:
      connection.close()

  def get_all_inputs(self):
    connection = self.connect()
    try:
      query = 'SELECT description FROM crimes;'
      with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        connection.close()

  def get_all_crimes(self):
    crimes = []
    connection = self.connect()
    try:
      query = 'SELECT category, date, latitude, longitude, description FROM crimes;'
      with connection.cursor() as cursor:
        cursor.execute(query)
        for row in cursor:
          crime = {
            'category': row[0],
            'date': datetime.datetime.strftime(row[1], '%Y-%m-%d'),
            'latitude': row[2],
            'longitude': row[3],
            'description': row[4]
          }
          crimes.append(crime)
    finally:
        connection.close()
    return crimes

  def add_crime(self, category, date, latitude, longitude, description):
    connection = self.connect()
    try:
      query = """INSERT INTO crimes (category, date, latitude, longitude, description)
                             VALUES (      %s,   %s,       %s,        %s,          %s);"""
      with connection.cursor() as cursor:
        cursor.execute(query, (category, date, latitude, longitude, description))
        connection.commit()
    except Exception as e:
      print(e)
    finally:
      connection.close()

  def clear_all(self):
    connection = self.connect()
    try:
      query = 'DELETE FROM crimes;'
      with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
    finally:
      connection.close()