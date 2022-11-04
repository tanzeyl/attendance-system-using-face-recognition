import cv2
from simple_facerec import SimpleFacerec
import mysql.connector

def addFace(sName, sEmail):
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    name = sName
    conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO `attendance` (`id`,`name`,`email`, `presentDays`, `workingDays`) VALUES (NULL,'{}','{}', 0, 0)""".format(sName, sEmail))
    conn.commit()
    cursor.execute("""SELECT * FROM `attendance` WHERE `id` = (SELECT MAX(`id`) FROM `attendance`)""")
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

    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
