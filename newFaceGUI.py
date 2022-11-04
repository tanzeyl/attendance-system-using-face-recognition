from tkinter import *
from addNewFace import addFace

def addNew():
  popUp = Tk()

  nameLabel = Label(popUp, text = "Enter the name:")
  nameLabel.grid(row = 0, column = 0)

  rollLabel = Label(popUp, text = "Enter the roll number:")
  rollLabel.grid(row = 1, column = 0)

  nameEntry = Entry(popUp, width = 50, borderwidth = 5)
  nameEntry.grid(row = 0, column = 1)

  rollEntry = Entry(popUp, width = 50, borderwidth = 5)
  rollEntry.grid(row = 1, column = 1)

  submitButton = Button(popUp, text = "Submit", padx = 50, pady = 10, command = lambda: addFace(nameEntry.get()))
  submitButton.grid(row = 2, column = 0, columnspan = 2)

  exitButton = Button(popUp, text = "Exit", padx = 50, pady = 10, command = popUp.quit)
  exitButton.grid(row = 3, column = 0, columnspan = 2)

  attention = Label(popUp, text = "After clicking on the Submit button, camera will open. Press 's' to capture a photo or 'q' to quit.")
  attention.grid(row = 4, column = 0)

  popUp.mainloop()
