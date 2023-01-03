import os
from tkinter import *
from PIL import ImageTk, Image
from newFaceGUI import addNew
import webbrowser
import importlib.util
import hashlib
import pymysql
from tkinter import filedialog
import cv2

conn = pymysql.connect(host="localhost", user="root", passwd="", database="attendanceDB")
cursor = conn.cursor()

spec2 = importlib.util.spec_from_file_location("simple_facerec", "simple_facerec.py")
module2 = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(module2)

spec = importlib.util.spec_from_file_location("RecognitionFromLiveFeed", "RecognitionFromLiveFeed.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = Tk()
app.title("Attendace System Using Face Recognition")
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.geometry(f"{width}x{height}")

global buttonToAddNewFace, buttonToLogin, buttonToOpenWebsite, buttonToTakeAttendance
emailExists = Label(app, text = "Email does not exist")
wrongPassword = Label(app, text = "Password Incorrect")

user = []

def openWebsite():
  url= 'http://127.0.0.1:5000/'
  webbrowser.open_new_tab(url)

def verifyLogin(email, password):
  flag = True
  password = hashlib.md5(password.encode()).hexdigest()
  cursor.execute("""SELECT * FROM `users` WHERE `email` = '{}'""".format(email))
  allData = cursor.fetchall()
  if len(allData) == 0:
      emailExists.grid(row = 5, column = 1)
      flag = False
  elif password != allData[0][4]:
      wrongPassword.grid(row = 5, column = 1)
      flag = False
  global tableName
  tableName = "attendance_" + email
  cursor.execute("""SELECT `name` FROM `users` WHERE `email` = '{}'""".format(email))
  allData = cursor.fetchall()
  name = allData[0][0]
  if (flag):
    emailExists.destroy()
    wrongPassword.destroy()
    top.destroy()
    buttonToLogin.destroy()
    buttonToTakeAttendance['state'] = NORMAL
    buttonToAddNewFace['state'] = NORMAL
    buttonToOpenWebsite['state'] = NORMAL
    buttonToselectFolder['state'] = NORMAL
    welcomeLabel = Label(app, text = f"Welcome {name}!").grid(row = 3, column = 1)

def login():
  global top
  top = Toplevel()
  global emailEntry, emailLabel, passwordEntry, passwordLabel, submitButton
  emailLabel = Label(top, text = "Enter the email: ")
  emailLabel.grid(row =0, column = 0)

  emailEntry = Entry(top, width = 50, borderwidth = 5)
  emailEntry.grid(row = 0, column = 1)

  passwordLabel = Label(top, text = "Enter the password: ")
  passwordLabel.grid(row = 1, column = 0)

  passwordEntry = Entry(top, show = "*", width = 50, borderwidth = 5)
  passwordEntry.grid(row = 1, column = 1)

  submitButton = Button(top, text = "Submit", padx = 50, pady = 10, command = lambda: verifyLogin(emailEntry.get(), passwordEntry.get()))
  submitButton.grid(row = 2, column = 0, columnspan = 2)

img = Image.open("C:\\Users\\tanze\\OneDrive\Desktop\\attendance-system-using-face-recognition\\GUI App\\background.jpg")
imgHeight = int(height/1.5)
img = img.resize((width, imgHeight))
img = ImageTk.PhotoImage(img)
label = Label(image = img).grid(row = 0, column = 0, columnspan = 4)

def browseFiles():
  count = 0
  filePath = filedialog.askdirectory()
  for root_dir, cur_dir, files in os.walk(filePath):
    count = len(files)
  for student in files:
    img = cv2.imread(filePath + "/" + student)
    data = student.split("_")
    email = data[0]
    name = data[1][:-4]
    cursor.execute("""INSERT INTO `{}` (`id`,`name`,`email`, `presentDays`, `workingDays`, `leaveDays`) VALUES (NULL,'{}','{}', 0, 0, 0)""".format("attendance_tanzeyl.khan@gmail.com", name, email))
    conn.commit()
    cursor.execute("""SELECT * FROM `{}` WHERE `id` = (SELECT MAX(`id`) FROM `{}`)""".format("attendance_tanzeyl.khan@gmail.com", "attendance_tanzeyl.khan@gmail.com"))
    student = cursor.fetchall()
    uniqueID = student[0][0]
    cv2.imwrite(filename = "images/" + str(uniqueID) + "_" + name + ".jpg", img = img)
    sfr = module2.SimpleFacerec()
    sfr.load_encoding_images("images/")
  countLabel = Label(app, text = f"{count} files found.").grid(row = 4, column = 1)

emptyLabel1 = Label(app, text = "").grid(row = 1, column = 1)

buttonToTakeAttendance = Button(app, text = "Take Attendance", padx = 10, pady = 10, command = lambda: module.attendance(tableName))
buttonToTakeAttendance.grid(row = 2, column = 0)
buttonToTakeAttendance['state'] = DISABLED

buttonToAddNewFace = Button(app, text = "Add new student", padx = 10, pady = 10, command = lambda: addNew(tableName))
buttonToAddNewFace.grid(row = 2, column = 1)
buttonToAddNewFace['state'] = DISABLED

buttonToOpenWebsite = Button(app, text = "Open Website", padx = 10, pady = 10, command = openWebsite)
buttonToOpenWebsite.grid(row = 2, column = 2)
buttonToOpenWebsite['state'] = DISABLED

buttonToselectFolder = Button(app, text = "Select Folder", padx = 10, pady = 10, command = browseFiles)
buttonToselectFolder.grid(row = 2, column = 3)
buttonToselectFolder['state'] = DISABLED

emptyLabel2 = Label(app, text = "").grid(row = 3, column = 1)

buttonToLogin = Button(app, text = "Login", padx = 30, pady = 10, command = login)
buttonToLogin.grid(row = 4, column = 1)

app.mainloop()
