import mysql.connector
import hashlib

# conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
# cursor = conn.cursor()
password = "abcd"
password = hashlib.md5(password.encode()).hexdigest()
print(password)
