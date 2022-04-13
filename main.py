import random
import boto3
import MySQLdb
import easygui
from secrets import access_key, secret_access_key
from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "123456"
clinet = boto3.client('s3',
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key)

ALLOWED_EXTENSIONS = {'mp4'}

app.config["MYSQL_HOST"] = "scalableservicesassignment.cz1kzfagdqhy.ap-south-1.rds.amazonaws.com"
app.config["MYSQL_USER"] = "admin"
app.config["MYSQL_PASSWORD"] = "123Amazon"
app.config["MYSQL_DB"] = "AdminInfo"

db = MySQL(app)


@app.route('/index')
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'email' in request.form and 'password' in request.form and 'Log In' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM AdminInfo.adminlogin WHERE email= %s AND Password = %s", (email, password))
            info = cursor.fetchone()

            if info is not None and info['Email'] == email and info['Password'] == password:
                session['loginsuccess'] = True
                return redirect(url_for('CourseAddition'))
            else:
                return "Login Error"

    return render_template("login.html")


@app.route('/CourseAddition', methods=['GET', 'POST'])
def CourseAddition():
    if request.method == 'POST':
        if 'course-name' in request.form and 'course-description' in request.form:
            courseName = request.form['course-name']
            courseDescription = request.form['course-description']
            courseVideoLink = coursefile
            easygui.msgbox("hi", title="simple gui")
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            choices = list(range(100))
            random.shuffle(choices)
            id = 2000 + choices.pop()
            cursor.execute("INSERT INTO Course.CourseVideo (ID, Title, Description, Link) VALUES (%s, %s, %s, %s)",
                           (id, courseName, courseDescription, courseVideoLink))
            db.connection.commit()
            easygui.msgbox("hi", title="simple gui")
            clinet = boto3.client('s3',
                                  aws_access_key_id=access_key,
                                  aws_secret_access_key=secret_access_key)
            upload_file_bucket = 'microsoftcoursevedio'
            upload_file_key = str(coursefile)
            clinet.upload_file(coursefile, upload_file_bucket, upload_file_key)

            return 'Registration Successful !!'

    elif session['loginsuccess']:
        return render_template("CourseAddition.html")

    else:
        return "Error"
@app.route('/upload',methods=['post'])
def upload():
    if request.method == 'POST':
        if 'course-name' in request.form and 'course-description' in request.form:
            video = request.files['file']
            if video:
                filename = secure_filename(video.filename)
                video.save(filename)
                upload_file_bucket = 'microsoftcoursevedio'
                clinet.upload_file(filename, upload_file_bucket, filename)
                easygui.msgbox("Uploded", title="simple gui")
                courseName = request.form['course-name']
                courseDescription = request.form['course-description']
                courseVideoLink = "https://d1kt47d0cneroo.cloudfront.net/"+filename.replace(" ", "+").replace("_", "+")
                cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
                choices = list(range(100))
                random.shuffle(choices)
                id = 2000 + choices.pop()
                cursor.execute("INSERT INTO Course.CourseVideo (ID, Title, Description, Link) VALUES (%s, %s, %s, %s)",
                               (id, courseName, courseDescription, courseVideoLink))
                db.connection.commit()
                msg = "Video Sucessfully Uploaded "
            return render_template("CourseAddition.html", msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
    app.run(debug=True)