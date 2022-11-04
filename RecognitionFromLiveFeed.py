import cv2
from simple_facerec import SimpleFacerec
import pandas as pd
from datetime import datetime

columns = ["Roll Number", "Name", "Time"]
data = pd.DataFrame(columns = columns)

sfr = SimpleFacerec()
sfr.load_encoded_images()

cap = cv2.VideoCapture(0)
presentList = []

while True:
  ret, frame = cap.read()
  face_locations, face_names = sfr.detect_known_faces(frame)
  for face_loc, name in zip(face_locations, face_names):
    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
    cv2.putText(frame, name, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)
    if name != "Unknown" and name not in presentList:
      presentList.append(name)
      time = datetime.now()
      time = time.strftime("%H:%M:%S")
      data.loc[len(data.index)] = [1, name, time]
      data.to_csv("Attendance.csv", index = False)

  cv2.imshow("Frame", frame)
  key = cv2.waitKey(1)
  if key == 27:
    break

cap.release()
cv2.destroyAllWindows()