import cv2
from simple_facerec import SimpleFacerec

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
name = input("Enter your name.\n")

while True:
    check, frame = webcam.read()
    cv2.imshow("Capturing", frame)
    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.imwrite(filename = "images/" + name + ".jpg", img = frame)
        print("Image saved!")
        break
    elif key == ord('q'):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

sfr = SimpleFacerec()
sfr.load_encoding_images("images/")
