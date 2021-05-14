import sql.connector as my
from flask import Flask, render_template,url_for,request

app = Flask(__name__)
@app.route('/enternow')
def new_student():
    return render_template('students.html')

@app.route('/addrec', methods = ['POST', 'GET'])
def new_student():
    if request.method = "POST":
        try:
            r = request.form['nm']
            r = request.form['add']
            r = request.form['city']
            r = request.form['pincode']

        db.connection = db.connect[host = "username",
                                   user = "root",
                                   password = "",
                                   database = "stud_details"]
                                   
