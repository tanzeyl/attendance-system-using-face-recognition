from flask import Flask, render_template, send_from_directory, send_file, request
import os
import mysql.connector
import pandas as pd
import smtplib
import os
import imghdr
from email.message import EmailMessage

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/download", methods = ["GET", "POST"])
def download_file():
    columns = ["Roll Number", "Name", "Email", "Present Days", "Working Days", "Leave Days"]
    cursor.execute("""SELECT * FROM `attendance`""")
    allData = cursor.fetchall()
    data = pd.DataFrame(allData, columns = columns)
    data.to_csv("uploads/All Data.csv", index = False)
    path = "uploads/All Data.csv"
    return send_file(path, as_attachment=True)

@app.route("/allStudents", methods = ["GET", "POST"])
def displayData():
    cursor.execute("""SELECT * FROM `attendance`""")
    allData = cursor.fetchall()
    return render_template('students.html', sList = allData)

@app.route("/sendEmail", methods = ["GET", "POST"])
def sendMail():
    if request.method == "POST":
        id = request.form.get("id")
        cursor.execute("""SELECT `email` FROM `attendance` WHERE `id` = {}""".format(id))
        allData = cursor.fetchall()
        email = allData[0][0]
        password = os.environ.get("PasswordMail")
        message = EmailMessage()
        message["Subject"] = "Warning! Low attendance."
        message["From"] = "ktanzeel80@gmail.com"
        message["To"] = email
        message.set_content("This is to inform you that your attendance is below 75%. Kindly get regular to your classes to avoid getting debarred.\nFind the file attached with this email, fill it and submit it to your respective HOD.")
        with open("uploads/Application.pdf", "rb") as file:
            fileData = file.read()
            fileName = file.name
        message.add_attachment(fileData, maintype = "application", subtype = "octet-stream", filename = fileName)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("ktanzeel80@gmail.com", password)
            smtp.send_message(message)
    cursor.execute("""SELECT * FROM `attendance`""")
    allData = cursor.fetchall()
    return render_template('students.html', sList = allData, message1 = True)

@app.route("/sendEmailToAll", methods = ["GET", "POST"])
def sendMailToAll():
    cursor.execute("""SELECT `email` FROM `attendance` WHERE presentDays/workingDays < 0.75""")
    allData = cursor.fetchall()
    emails = []
    for row in allData:
        emails.append(row[0])
    password = os.environ.get("PasswordMail")
    message = EmailMessage()
    message["Subject"] = "Warning! Low attendance."
    message["From"] = "ktanzeel80@gmail.com"
    message["To"] = emails
    message.set_content("This is to inform you that your attendance is below 75%. Kindly get regular to your classes to avoid getting debarred.\nFind the file attached with this email, fill it and submit it to your respective HOD.")
    with open("uploads/Application.pdf", "rb") as file:
        fileData = file.read()
        fileName = file.name
    message.add_attachment(fileData, maintype = "application", subtype = "octet-stream", filename = fileName)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("ktanzeel80@gmail.com", password)
        smtp.send_message(message)
    cursor.execute("""SELECT * FROM `attendance`""")
    allData = cursor.fetchall()
    return render_template('students.html', sList = allData, message2 = True)

@app.route("/addMedicalLeave", methods=['GET', 'POST'])
def selectStudent():
    cursor.execute("""SELECT * FROM `attendance`""")
    allData = cursor.fetchall()
    return render_template('selectStudent.html', sList = allData)

@app.route("/addMedical", methods = ["GET", "POST"])
def getMedicalInfo():
    if request.method == "POST":
        id = request.form.get("id")
        days = request.form.get("days")
        cursor.execute("""UPDATE `attendance` SET `leaveDays` = {} WHERE `id` = {}""".format(days, id))
        conn.commit()
    cursor.execute("""SELECT * FROM `attendance`""")
    allData = cursor.fetchall()
    return render_template('selectStudent.html', sList = allData, message1 = True)

@app.route("/search", methods = ["GET", "POST"])
def searchStudents():
    if request.method == "POST":
        name = request.form.get("query")
    name = name.capitalize()
    cursor.execute("""SELECT * FROM `attendance` WHERE `name` LIKE '%{}%'""".format(name))
    allData = cursor.fetchall()
    return render_template('selectStudent.html', sList = allData)

if __name__ == "__main__":
    app.run(debug = True)
