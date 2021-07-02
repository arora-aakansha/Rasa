import sqlite3

conn = sqlite3.connect('rasa.db')

print("connected")

class Repo:

  @staticmethod
  def initDb():
    conn.execute('''
        CREATE TABLE IF NOT EXISTS  demo (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            EMPLOYEE_CODE TEXT UNIQUE NOT NULL,
            EMAIL TEXT UNIQUE NOT NULL
        );
    ''')
    conn.commit()

  
  @staticmethod
  def insert(name, emp_code, email):
    conn.execute('''
      INSERT INTO demo (NAME, EMPLOYEE_CODE, EMAIL) VALUES (?, ?, ?);
    ''', (name, emp_code, email))
    conn.commit()


  @staticmethod
  def select():

    cur = conn.cursor()

    cur.execute('''
      SELECT * FROM demo;
    ''')

    rows = cur.fetchall()

    return str(rows).strip('[]') if len(rows) > 0 else "No records found"

  @staticmethod
  def delete(value):
    #conn.execute("DELETE FROM demo WHERE EMPLOYEE_CODE='{value}'")
    conn.execute(f"DELETE FROM demo WHERE EMPLOYEE_CODE='{value}'")
    conn.commit()