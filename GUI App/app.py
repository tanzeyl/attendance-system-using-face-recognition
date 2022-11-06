from tkinter import *
from PIL import ImageTk, Image
from newFaceGUI import addNew
import webbrowser
import importlib.util

spec = importlib.util.spec_from_file_location("RecognitionFromLiveFeed", "RecognitionFromLiveFeed.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = Tk()
app.title("Attendace System Using Face Recognition")

def openWebsite():
  url= 'https://github.com/tanzeyl'
  webbrowser.open_new_tab(url)

img = ImageTk.PhotoImage(Image.open("C:\\Users\\tanze\\OneDrive\Desktop\\attendance-system-using-face-recognition\\GUI App\\background.jpg"))
label = Label(image = img).grid(row = 0, column = 0, columnspan = 3)

buttonToTakeAttendance = Button(app, text = "Take Attendance", padx = 10, pady = 10, command = module.attendance)
buttonToTakeAttendance.grid(row = 1, column = 0)

buttonToAddNewFace = Button(app, text = "Add new student", padx = 10, pady = 10, command = addNew)
buttonToAddNewFace.grid(row = 1, column = 1)

buttonToOpenWebsite = Button(app, text = "Open Website", padx = 10, pady = 10, command = openWebsite)
buttonToOpenWebsite.grid(row = 1, column = 2)
app.mainloop()
