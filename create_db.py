import sys
import os
import sqlite3

DBExist = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()


def main(argv):
    if not DBExist:
        create_tables()

        inputFileName = argv[1]
    
        with open(inputFileName) as inputfile:
            for currline in inputfile:
                s = currline.strip().split(',')
                if currline[0] == "C":
                    insert_course(s[1], s[2].strip(), s[3].strip(),  s[4], s[5], s[6])
                elif currline[0] == "R":
                    insert_classrooms(s[1], s[2].strip(), 0, 0)
                else:
                    insert_students(s[1].strip(), s[2])
    print_table_as_a_table("courses")
    print_table_as_a_table("classrooms")
    print_table_as_a_table("students")
    close_db()


def print_table_as_a_table(table):
    cursor.execute('SELECT * FROM ' + table)
    list = cursor.fetchall()

    print(table)
    i = 0
    for item in list:
        i = i + 1
        print(str(item))


def create_tables():
    if not DBExist:
        cursor.execute(""" CREATE TABLE courses(id INTEGER PRIMARY KEY,
                                  course_name  TEXT NOT NULL,
                                  student TEXT NOT NULL,
                                  number_of_students INTEGER NOT NULL,
                                  class_id INTEGER REFERENCES classrooms(id),
                                  course_length INTEGER NOT NULL
                                  )
                                                """)
        cursor.execute(""" CREATE TABLE students(
                                  grade TEXT PRIMARY KEY,
                                  count INTEGER NOT NULL
                                )
                                                """)
        cursor.execute(""" CREATE TABLE classrooms(
                                  id INTEGER PRIMARY KEY,
                                  location TEXT NOT NULL,
                                  current_course_id INTEGER NOT NULL,
                                  current_course_time_left INTEGER NOT NULL
                                )
                                                """)


def insert_course(id, name, student, numStudents, classId, length):
    cursor.execute("INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?)", [id, name, student, numStudents, classId, length])


def insert_students(grade, count):
    cursor.execute("INSERT INTO students VALUES (?, ?)", [grade, count])


def insert_classrooms(id, location, currCourseId, currCourseTimeLeft):
    cursor.execute("INSERT INTO classrooms VALUES (?, ?, ?, ?)", [id, location, currCourseId, currCourseTimeLeft])


def close_db():
    dbcon.commit()
    dbcon.close()


if __name__ == '__main__':
    main(sys.argv)
