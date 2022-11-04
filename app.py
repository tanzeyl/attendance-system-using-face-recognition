from tkinter import *
from PIL import ImageTk, Image
from RecognitionFromLiveFeed import attendance
from newFaceGUI import addNew

app = Tk()
app.title("Attendace System Using Face Recognition")


img = ImageTk.PhotoImage(Image.open("C:\\Users\\tanze\\OneDrive\\Desktop\\attendance-system-using-face-recognition\\assets\\background.jpg"))
label = Label(image = img).grid(row = 0, column = 0, columnspan = 3)

buttonToTakeAttendance = Button(app, text = "Take Attendance", padx = 50, pady = 10, command = attendance)
buttonToTakeAttendance.grid(row = 1, column = 0)

buttonToAddNewFace = Button(app, text = "Add new student", padx = 50, pady = 10, command = addNew)
buttonToAddNewFace.grid(row = 1, column = 1)
app.mainloop()
