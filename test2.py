import smtplib
import os
import imghdr
from email.message import EmailMessage

password = os.environ.get("PasswordMail")

message = EmailMessage()
message["Subject"] = "Warning! Low attendance."
message["From"] = "ktanzeel80@gmail.com"
message["To"] = "tanzeyl.khan@gmail.com"
message.set_content("This is to inform you that your attendance is below 75%. Kindly get regular to your classes to avoid getting debarred.\nFind the file attached with this email, fill it and submit it to your respective HOD.")

with open("Application.pdf", "rb") as file:
  fileData = file.read()
  fileName = file.name

message.add_attachment(fileData, maintype = "application", subtype = "octet-stream", filename = fileName)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
  smtp.login("ktanzeel80@gmail.com", password)
  smtp.send_message(message)
