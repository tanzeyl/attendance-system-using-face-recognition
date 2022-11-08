import cv2
import mysql.connector
import importlib.util

spec = importlib.util.spec_from_file_location("simple_facerec", "simple_facerec.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()

def addFace(sName, sEmail, tableName):
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    name = sName
    cursor.execute("""INSERT INTO `{}` (`id`,`name`,`email`, `presentDays`, `workingDays`, `leaveDays`) VALUES (NULL,'{}','{}', 0, 0, 0)""".format(tableName, sName, sEmail))
    conn.commit()
    cursor.execute("""SELECT * FROM `{}` WHERE `id` = (SELECT MAX(`id`) FROM `{}`)""".format(tableName, tableName))
    student = cursor.fetchall()
    uniqueID = student[0][0]
    while True:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename = "images/" + str(uniqueID) + "_" + name + ".jpg", img = frame)
            cv2.destroyAllWindows()
            break

    sfr = module.SimpleFacerec()
    sfr.load_encoding_images("images/")
