import cv2
from simple_facerec import SimpleFacerec
import pandas as pd
from datetime import datetime
import mysql.connector

def attendance():
  conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
  cursor = conn.cursor()

  columns = ["Roll Number", "Name", "Time"]
  data = pd.DataFrame(columns = columns)

  sfr = SimpleFacerec()
  sfr.load_encoded_images()

  cap = cv2.VideoCapture(0)
  presentList = []
  marked = {}

  while True:
    ret, frame = cap.read()
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
      y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
      cv2.putText(frame, name, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
      cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)
      if name != "Unknown" and name not in presentList:
        presentList.append(name)
        marked[name] = True
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        data.loc[len(data.index)] = [1, name, time]
        data.to_csv("Attendance.csv", index = False)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
      break

  for name in presentList:
    name = name.split("_")
    id = name[0]
    name = name[1][:-4]
    cursor.execute("""UPDATE `attendance` SET `presentDays` = `presentDays` + 1 WHERE `id` = {}""".format(id))
    conn.commit()

  cursor.execute("""SELECT `id` FROM `attendance`""")
  idList = cursor.fetchall()

  for row in idList:
    cursor.execute("""UPDATE `attendance` SET `workingDays` = `workingDays` + 1 WHERE `id` = {}""".format(row[0]))
    conn.commit()

  cap.release()
  cv2.destroyAllWindows()
