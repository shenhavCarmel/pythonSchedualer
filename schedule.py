import os
import sqlite3

DBExist = os.path.isfile('schedule.db')
dbcon = sqlite3.connect('schedule.db')
cursor = dbcon.cursor()
iteration_num = 0


def main():
    global iteration_num
    if DBExist and (len(cursor.execute("SELECT * FROM courses").fetchall()) > 0):
        while DBExist and (len(cursor.execute("SELECT * FROM courses").fetchall()) > 0):
            classes_list = cursor.execute("SELECT * FROM classrooms").fetchall()
            for currClass in classes_list:
                if currClass[3] == 0:
                    assign_new_course(currClass[0], currClass[1])
                else:

                    # print
                    in_class_course_name = cursor.execute("SELECT course_name FROM courses WHERE id = (?)", [currClass[2]]).fetchone()[0]

                    # Decrease by 1 current_course_time_left in the classrooms table
                    cursor.execute("UPDATE classrooms SET current_course_time_left = (?) WHERE id = (?)", [currClass[3]-1, currClass[0]])

                    if currClass[3]-1 == 0:
                        print("({}) {}: {} is done".format(iteration_num, currClass[1], in_class_course_name))

                        # Remove the course from the DB
                        cursor.execute("DELETE FROM courses WHERE id = (?)", [currClass[2]])

                        # Update classroom current course id to be nothing
                        cursor.execute("UPDATE classrooms SET current_course_id = (?) WHERE id = (?)", [0, currClass[0]])

                        # assign a new course to the classroom
                        assign_new_course(currClass[0], currClass[1])
                    else:
                        print("({}) {}: occupied by {}".format(iteration_num, currClass[1], in_class_course_name))

            iteration_num += 1

            print_table_as_a_table("courses")
            print_table_as_a_table("classrooms")
            print_table_as_a_table("students")

        close_db()
    else:
        print_table_as_a_table("courses")
        print_table_as_a_table("classrooms")
        print_table_as_a_table("students")
        close_db()


def assign_new_course(class_id, class_location):
    global iteration_num
    course = cursor.execute("SELECT * FROM courses WHERE class_id = (?)", [class_id]).fetchone()
    if not course is None:
        course_to_enter_id = course[0]
        course_to_enter_name = course[1]
        course_to_enter_length = course[5]

        print("({}) {}: {} is schedule to start".format(iteration_num, class_location, course_to_enter_name))

        deduct_students(course_to_enter_id)

        # upfate classes table
        cursor.execute("UPDATE classrooms SET current_course_id = (?), current_course_time_left = (?) WHERE id = (?)", [course_to_enter_id, course_to_enter_length, class_id])


def deduct_students(course_id):
    global iteration_num
    course_info = cursor.execute("SELECT student, number_of_students FROM courses WHERE id = (?)", [course_id]).fetchone()
    student_grade = course_info[0]
    num_students_course = course_info[1]
    count_students = cursor.execute("SELECT count FROM students WHERE grade = (?)", [student_grade]).fetchone()[0]
    if count_students < num_students_course:
        # update to 0
        cursor.execute("UPDATE students SET count = 0 WHERE grade = (?)", [student_grade])
    else:
        cursor.execute("UPDATE students SET count = (?) WHERE grade = (?)", [count_students-num_students_course, student_grade])


def print_table_as_a_table(table):
    cursor.execute('SELECT * FROM ' + table)
    list = cursor.fetchall()

    print(table)
    i = 0
    for item in list:
        i = i + 1
        print(str(item))


def close_db():
    dbcon.commit()
    dbcon.close()


if __name__ == '__main__':
    main()