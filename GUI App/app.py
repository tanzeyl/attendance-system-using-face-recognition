from tkinter import *
from PIL import ImageTk, Image
from newFaceGUI import addNew
import webbrowser
import importlib.util
import hashlib
import mysql.connector

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()


spec = importlib.util.spec_from_file_location("RecognitionFromLiveFeed", "RecognitionFromLiveFeed.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = Tk()
app.title("Attendace System Using Face Recognition")

user = []

def openWebsite():
  url= 'http://127.0.0.1:5000/'
  webbrowser.open_new_tab(url)

def verifyLogin(email, password):
  password = hashlib.md5(password.encode()).hexdigest()
  cursor.execute("""SELECT * FROM `users` WHERE `email` = '{}'""".format(email))
  allData = cursor.fetchall()
  if password != allData[0][4]:
      wrongPassword = Label(app, text = "Password Incorrect").grid(row = 4, column = 1)
  elif len(allData) == 0:
      emailExists = Label(app, text = "Email does not exist").grid(row = 4, column = 1)
  global tableName
  tableName = "attendance_" + email
  cursor.execute("""SELECT `name` FROM `users` WHERE `email` = '{}'""".format(email))
  allData = cursor.fetchall()
  name = allData[0][0]
  welcomeLabel = Label(app, text = f"Welcome {name}!").grid(row = 3, column = 1)

def login():
  top = Toplevel()
  global emailEntry, emailLabel, passwordEntry, passwordLabel, submitButton
  emailLabel = Label(top, text = "Enter the email: ")
  emailLabel.grid(row =0, column = 0)

  emailEntry = Entry(top, width = 50, borderwidth = 5)
  emailEntry.grid(row = 0, column = 1)

  passwordLabel = Label(top, text = "Enter the password: ")
  passwordLabel.grid(row = 1, column = 0)

  passwordEntry = Entry(top, width = 50, borderwidth = 5)
  passwordEntry.grid(row = 1, column = 1)

  submitButton = Button(top, text = "Submit", padx = 50, pady = 10, command = lambda: verifyLogin(emailEntry.get(), passwordEntry.get()))
  submitButton.grid(row = 2, column = 0, columnspan = 2)

  exitButton = Button(top, text = "Close", padx = 50, pady = 10, command = top.destroy)
  exitButton.grid(row = 3, column = 0, columnspan = 2)

img = ImageTk.PhotoImage(Image.open("C:\\Users\\tanze\\OneDrive\Desktop\\attendance-system-using-face-recognition\\GUI App\\background.jpg"))
label = Label(image = img).grid(row = 0, column = 0, columnspan = 3)

buttonToTakeAttendance = Button(app, text = "Take Attendance", padx = 10, pady = 10, command = lambda: module.attendance(tableName))
buttonToTakeAttendance.grid(row = 1, column = 0)

buttonToAddNewFace = Button(app, text = "Add new student", padx = 10, pady = 10, command = lambda: addNew(tableName))
buttonToAddNewFace.grid(row = 1, column = 1)

buttonToOpenWebsite = Button(app, text = "Open Website", padx = 10, pady = 10, command = openWebsite)
buttonToOpenWebsite.grid(row = 1, column = 2)

buttonToLogin = Button(app, text = "Login", padx = 30, pady = 10, command = login)
buttonToLogin.grid(row = 2, column = 1)

app.mainloop()
