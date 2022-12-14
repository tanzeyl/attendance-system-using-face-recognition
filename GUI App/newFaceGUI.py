from tkinter import *
import importlib.util

spec = importlib.util.spec_from_file_location("addNewFace", "addNewFace.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def addNew(tableName):
  popUp = Tk()
  popUp.title("Add a new Student")

  nameLabel = Label(popUp, text = "Enter the name:")
  nameLabel.grid(row = 0, column = 0)

  emailLabel = Label(popUp, text = "Enter the email:")
  emailLabel.grid(row = 1, column = 0)

  nameEntry = Entry(popUp, width = 50, borderwidth = 5)
  nameEntry.grid(row = 0, column = 1)

  emailEntry = Entry(popUp, width = 50, borderwidth = 5)
  emailEntry.grid(row = 1, column = 1)

  submitButton = Button(popUp, text = "Submit", padx = 50, pady = 10, command = lambda: module.addFace(nameEntry.get(), emailEntry.get(), tableName))
  submitButton.grid(row = 2, column = 0, columnspan = 2)

  exitButton = Button(popUp, text = "Exit", padx = 50, pady = 10, command = popUp.destroy)
  exitButton.grid(row = 3, column = 0, columnspan = 2)

  attention = Label(popUp, text = "After clicking on the Submit button, camera will open. Press 's' to capture a photo or 'q' to quit.")
  attention.grid(row = 4, column = 0)

  popUp.mainloop()
