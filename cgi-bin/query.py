import pymysql
import sys

ini = sys.argv[1]
hostname = sys.argv[2]
port = sys.argv[3]
ini = ini.split("&")
student_id = ini[0].split("=")[1]
student_name = ini[1].split("=")[1]
student_class = ini[2].split("=")[1]
value = " (" + student_id + ',"' + student_name + '","' + student_class + '")'

db = pymysql.connect(host="localhost",
                     user="root",
                     password="root",
                     database="Student_data",
                     charset='utf8')
cursor = db.cursor()

try:
    sql = "INSERT INTO student(student_id,student_name,student_class) values" + value + ";"
    cursor.execute(sql)
    db.commit()
except:
    db.rollback()

cursor.execute("SELECT * from student order by student_id;")

data = cursor.fetchall()
res = ""
with open("cgi-bin/query.html", "r", encoding="utf-8") as f:
    for line in f:
        res += line
student_data = ''
for student in data:
    temp = "<tr>"
    temp += "<th>" + str(student[0]) + "</th>"
    temp += "<th>" + student[1] + "</th>"
    temp += "<th>" + student[2] + "</th>"
    temp += "</tr>\n"
    student_data += temp
res = res.replace("$data", student_data)

print(res)