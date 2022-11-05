import mysql.connector
import pandas as pd

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()

cursor.execute("""SELECT * FROM `attendance`""")
idList = cursor.fetchall()

data = pd.DataFrame(idList)
data.to_csv("All Data.csv", index = False)
