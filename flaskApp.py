from flask import Flask, render_template, send_file, request, session
import os
import pymysql
import pandas as pd
import smtplib
import os
from email.message import EmailMessage
import hashlib

conn = pymysql.connect(host="localhost", user="root", passwd="", database="attendanceDB")
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods = ["GET", "POST"])
def signup():
    return render_template("signup.html")

@app.route("/verifySignup", methods = ["GET", "POST"])
def getInfo():
    name = request.form.get("name")
    email = request.form.get("email")
    college = request.form.get("college")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")
    if (password != confirmPassword):
        return render_template("signup.html", message1 = True)
    cursor.execute("""SELECT `email` FROM `users` WHERE `email` = '{}'""".format(email))
    allData = cursor.fetchall()
    if (len(allData) != 0):
        return render_template("signup.html", message2 = True)
    password = hashlib.md5(password.encode()).hexdigest()
    cursor.execute("""INSERT INTO `users` (`id`, `name`, `email`, `college`, `password`) VALUES (NULL, '{}', '{}', '{}', '{}')""".format(name, email, college, password))
    conn.commit()
    tableName = "attendance_" + email
    session['tableName'] = tableName
    session['user'] = name
    session['email'] = email
    cursor.execute("""CREATE TABLE `{}` (
        `id` int(10) not null auto_increment primary key,
        `name` varchar(255),
        `email` varchar(255),
        `presentDays` int(10),
        `workingDays` int(10),
        `leaveDays` int(10)
    )""".format(tableName))
    conn.commit()
    return render_template("index.html", user = session['user'])

@app.route("/verifyLogin", methods = ["GET", "POST"])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")
    password = hashlib.md5(password.encode()).hexdigest()
    cursor.execute("""SELECT * FROM `users` WHERE `email` = '{}'""".format(email))
    allData = cursor.fetchall()
    if password != allData[0][4]:
        return render_template("login.html", message1 = True)
    elif len(allData) == 0:
        return render_template("login.html", message2 = True)
    tableName = "attendance_" + email
    session['tableName'] = tableName
    session['user'] = allData[0][1]
    session['email'] = email
    return render_template("index.html", user = session["user"])

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/dashboard", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/download", methods = ["GET", "POST"])
def download_file():
    columns = ["Roll Number", "Name", "Email", "Present Days", "Working Days", "Leave Days"]
    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    data = pd.DataFrame(allData, columns = columns)
    data.to_csv("uploads/All Data.csv", index = False)
    path = "uploads/All Data.csv"
    return send_file(path, as_attachment=True)

@app.route("/allStudents", methods = ["GET", "POST"])
def displayData():
    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    return render_template('students.html', sList = allData)

@app.route("/sendEmail", methods = ["GET", "POST"])
def sendMail():
    if request.method == "POST":
        id = request.form.get("id")
        cursor.execute("""SELECT `email` FROM `{}` WHERE `id` = {}""".format(session["tableName"], id))
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

    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    return render_template('students.html', sList = allData, message1 = True)

@app.route("/sendEmailToAll", methods = ["GET", "POST"])
def sendMailToAll():
    cursor.execute("""SELECT `email` FROM `{}` WHERE presentDays/workingDays < 0.75""".format(session["tableName"]))
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

    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    return render_template('students.html', sList = allData, message2 = True)

@app.route("/addMedicalLeave", methods=['GET', 'POST'])
def selectStudent():
    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    return render_template('selectStudent.html', sList = allData)

@app.route("/addMedical", methods = ["GET", "POST"])
def getMedicalInfo():
    if request.method == "POST":
        id = request.form.get("id")
        days = request.form.get("days")
        cursor.execute("""UPDATE `{}` SET `leaveDays` = {} WHERE `id` = {}""".format(session["tableName"], days, id))
        conn.commit()
    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    return render_template('selectStudent.html', sList = allData, message1 = True)

@app.route("/search", methods = ["GET", "POST"])
def searchStudents():
    if request.method == "POST":
        name = request.form.get("query")
    name = name.capitalize()
    cursor.execute("""SELECT * FROM `{}` WHERE `name` LIKE '%{}%'""".format(session["tableName"], name))
    allData = cursor.fetchall()
    return render_template('selectStudent.html', sList = allData)

@app.route("/aboutUs", methods = ["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/password", methods = ["GET", "POST"])
def change():
    return render_template("change.html")

@app.route("/changePassword", methods = ["GET", "POST"])
def passwordChange():
    oldP = request.form.get("oldP")
    newP = request.form.get("newP")
    confNewP = request.form.get("confNewP")
    cursor.execute("""SELECT `password` FROM `users` WHERE `email` = '{}'""".format(session['email']))
    allData = cursor.fetchall()
    password = allData[0][0]
    oldP = hashlib.md5(oldP.encode()).hexdigest()
    if (oldP != password):
        return render_template("change.html", message1 = True)
    elif (newP != confNewP):
        return render_template("change.html", message2 = True)
    newP = hashlib.md5(newP.encode()).hexdigest()
    cursor.execute("""UPDATE `users` SET `password` = '{}' WHERE `email` = '{}'""".format(newP, session["email"]))
    conn.commit()
    return render_template("index.html", message1 = True, user = session["user"])

@app.route("/broadcast", methods = ["GET", "POST"])
def formBroadcastMessage():
    return render_template("formMessage.html")

@app.route("/collectMessageData", methods = ["GET", "POST"])
def sendEmail():
    header = request.form.get("header")
    body = request.form.get("body")
    f = request.files['file']
    cursor.execute("""SELECT `email` FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    emails = []
    for row in allData:
        emails.append(row[0])
    password = os.environ.get("PasswordMail")
    message = EmailMessage()
    message["Subject"] = header
    message["From"] = "ktanzeel80@gmail.com"
    message["To"] = emails
    message.set_content(body)
    with open("uploads/CustomAttachment.pdf", "rb") as file:
        fileData = file.read()
        fileName = file.name
    message.add_attachment(fileData, maintype = "application", subtype = "octet-stream", filename = fileName)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("ktanzeel80@gmail.com", password)
        smtp.send_message(message)
    cursor.execute("""SELECT * FROM `{}`""".format(session["tableName"]))
    allData = cursor.fetchall()
    return render_template('index.html', message2 = True)

if __name__ == "__main__":
    app.run(debug = False, host = "0.0.0.0")
