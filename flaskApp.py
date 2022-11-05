from flask import Flask, render_template, send_from_directory, send_file
import os
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(host="remotemysql.com", user="aYGuuyn6NF", passwd="Ok1yVANkD7", database="aYGuuyn6NF")
cursor = conn.cursor()

UPLOAD_FOLDER = "UPLOAD_FOLDER"

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/download", methods=["GET", "POST"])
def download_file():
	path = "All Data.csv"
	return send_file(path, as_attachment=True)

@app.route("/download", methods=["GET", "POST"])
def download_file():
	path = "All Data.csv"
	return send_file(path, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)
