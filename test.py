import mysql.connector

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()

cursor.execute("""SELECT `id` FROM `attendance`""")
idList = cursor.fetchall()

for row in idList:
  cursor.execute("""UPDATE `attendance` SET `workingDays` = `workingDays` + 1 WHERE `id` = {}""".format(row[0]))
  conn.commit()
