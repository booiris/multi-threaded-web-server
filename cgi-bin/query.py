import pymysql
# import sys

# ini = sys.argv[1]
# hostname = sys.argv[2]
# port = sys.argv[3]

db = pymysql.connect(host="localhost",
                     user="root",
                     password="root",
                     database="Student_data",
                     charset='utf8')
cursor = db.cursor()

try:
    cursor.execute(
        "INSERT INTO student(student_id,student_name) values (123,'empty')")
    db.commit()
except:
    print("wrong")
    db.rollback()

cursor.execute("SELECT * from student")

data = cursor.fetchall()

print(data)