import cv2
from simple_facerec import SimpleFacerec

def addFace(sName):
    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    name = sName

    while True:
        check, frame = webcam.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename = "images/" + name + ".jpg", img = frame)
            print("Image saved!")
            cv2.destroyAllWindows()
            break

    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")
