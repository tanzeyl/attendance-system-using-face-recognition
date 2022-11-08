import mysql.connector
import hashlib

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()
email = "tanzeyl.khan@gmail.com"
cursor.execute("""SELECT * FROM `users` WHERE `email` = '{}'""".format(email))
allData = cursor.fetchall()
print(allData)
