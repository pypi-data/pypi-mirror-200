from openpysql import OpenPySQL


def test_sql():

    db = OpenPySQL.sqlite('test.db')

    db.query = """
        CREATE TABLE students (
            student_id  INTEGER  PRIMARY KEY,
            first_name  TEXT     NOT NULL,
            last_name   TEXT     NOT NULL,
            gender      TEXT     NOT NULL
        );"""
    db.value = None
    db.execute()

    db.query = "INSERT INTO students (first_name, last_name, gender) VALUES (?, ?, ?);"
    db.value = ('Eloise', 'Robinson', 'F')
    db.execute()

    db.query = "INSERT INTO students (first_name, last_name, gender) VALUES (?, ?, ?);"
    db.value = [
        ('Jakob', 'Bryant', 'M'),
        ('Hannah', 'Mcgee', 'F'),
    ]
    db.execute()

    db.query = "SELECT * FROM students WHERE gender=?;"
    db.value = 'F'
    db.fetch(0)
    db.fetch(1)

    db.close()


def test_password():
    hash = OpenPySQL.hashpw('helloworld')
    assert OpenPySQL.checkpw('helloworld', hash) == True
