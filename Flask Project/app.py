import mysql.connector as db
from flask import Flask, render_template,url_for,request,redirect,session,sessions
import re

app=Flask(__name__)
app.secret_key = 'secret key'

@app.route('/registration', methods=['GET','POST'])
def registration():

    db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
    if request.method=='POST':
        id = request.form['emp_id']
        password = request.form['password']
        password2 = request.form['password-repeat']
        cur=db.connection.cursor(buffered=True)
     
        cur.execute("SELECT * from account where emp_id={}".format(id))
        duplicate_id =cur.fetchone()


        
        if duplicate_id:
            msg= "Account already exists!. Please Log In"
        elif password!=password2:
            msg="Password doesn't match"
        elif not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",password):
            msg= 'Password should contain minimum 8 characters and one number'
        
        else:
            cur=db.connection.cursor()
            cur.execute("Insert into account (emp_id,emp_password) values ({}, '{}')".format(id,password))
            db.connection.commit()
            return redirect(url_for('login'))
        return render_template('registration.html', msg=msg)
    

    else:
        
        return render_template('registration.html')
    

@app.route('/', methods=['GET','POST'])
def login():
    
    db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
    

    if request.method=='POST':
        id= request.form['emp_id'] 
        password= request.form['psw'] 
        #db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
        cur=db.connection.cursor(buffered=True)
        cur.execute("SELECT * from account where emp_id={} and emp_password='{}' ".format(id,password))
        account=cur.fetchone()

        if account: 
            session['id'] = 'id'
            
            cur.execute("SELECT * from employee_details where id1={} ".format(id))
            records=cur.fetchall()
            if records:
                r=records[0][1]
                rec=records
                return render_template('employee_list.html',records=r, rec=rec)
            else:
                msg="No entry in the database. Please contact Administrator"
                return render_template('employee_list.html',msg=msg)

          
        else:
            msg1="Invalid UserName or Password"
            return render_template('loginpage.html',msg=msg1)

    else:
        if 'id' in session:
            return redirect('request.url')

            #return redirect(url_for('login'))
        return render_template('loginpage.html')

    #except Exception as error:
        #msg = "Error while logging in! Please try again later"
        #return render_template('error.html',msg=msg)
        

@app.route('/admin', methods=['GET','POST'])
def admin():
    
    if request.method=='POST':
        if request.form['admin_username']=='admin' and request.form['psw']=='admin123':
           session['username'] = 'admin'
           #db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
           #cur=db.connection.cursor()
           #cur.execute("SELECT * from employee_details")
           #r=cur.fetchall()
           return redirect(url_for('home'))
        else:
            msg="Invalid Username or Password"
            return render_template('admin.html',msg=msg)
            
            

    else:
        if 'username' in session:
            return redirect(url_for('home'))
        return render_template('admin.html')
 
    

@app.route('/logout')
def logout(): 
    try:
        session.pop('username', None) 
        session.pop('id', None) 
        return redirect(url_for('login')) 

    except Exception as error:
        return "Error!! Please try again."


@app.route('/adminlogout')
def adminlogout(): 
    session.pop('username', None) 
  
    
    return render_template('admin.html') 


@app.route('/home', methods=['POST','GET'])
def home():
    try:
        if 'username' in session:
            db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
            cur=db.connection.cursor()
            cur.execute("SELECT * from employee_details order by id1")
            r=cur.fetchall()
            
            return render_template('index.html',records=r)


        return redirect(url_for('admin'))


    except Exception as error:
        return "Error!! Please try again."


@app.route('/add_employee', methods=['GET','POST'])
def add_employee():
    if 'username' in session:
        if request.method=='POST':
            db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
            id=request.form['id']
            name=request.form['name']
            email=request.form['email']
            address=request.form['add']
            contact=request.form['contact']
            salary=request.form['salary']
            department=request.form['department']
            
                
            cur=db.connection.cursor(buffered=True)
            cur.execute("SELECT id1 from employee_details")
            duplicate_account=cur.fetchone()
            cur.execute("SELECT contact from employee_details")
            duplicate_contact=cur.fetchall()
            cur.execute("SELECT email from employee_details")
            duplicate_email=cur.fetchone()
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 

            
            if id in duplicate_account:
                    msg="Duplicate Id Entry"    
            elif contact in duplicate_contact:
                    msg="Duplicate Contact Entry"
            elif email in duplicate_email:
                    msg="Duplicate Email Entry"  
            elif id == "":
                msg= "Please Enter ID"
            elif name == "":
                msg= "Please Enter Name"
            elif email == "":
                msg= "Please Enter Email"
            elif contact == "":
                msg= "Please Enter Contact"
            elif salary == "":
                msg= "Please Enter Salary"
            elif department == "":
                msg= "Please Enter Department"
            elif name.isdigit()==True and regex.search(name) != None:
                msg="Invalid Name"
            elif contact== "":
                msg="Please fill contact"
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email): 
                msg = 'Invalid email address !'
            elif len(contact)!=10 and contact.isdigit()==False:
                msg="Invalid contact"
                
            else:
                db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
                cur=db.connection.cursor()
                cur.execute("Insert into employee_details values({}, '{}','{}','{}','{}',{},'{}')".format(id, name, email,address,contact,salary,department))
                db.connection.commit()
                return redirect(url_for('home'))
            return render_template ('emp_form.html',msg=msg)
            
            
            

           
        else:
            return render_template ('emp_form.html')

    elif 'username' not in session:
        return redirect(url_for('admin'))

    


        
       
'''
@app.route('/edit_employee<int:id1>',methods=['GET','POST'])
def edit_employee(id1):
    db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
    if request.method=='POST':
        newid = request.form.get("newid")
        oldid = request.form.get("oldid")
        cur.execute("UPDATE employee_details SET id={} WHERE id={}".format(newid,oldid))
        return redirect("/")
    else:
        id=id1
        cur=db.connection.cursor()
        cur.execute("SELECT * from employee_details WHERE id1={}".format(id))
        r=cur.fetchall()

        return render_template('update.html',records=r)
'''

@app.route("/editUser" , methods=['POST','GET'])
def editUser():
    
    db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
    if request.method=='POST':
        id=request.args.get("id")
        name1=request.form['name']
        email1=request.form['email']
        address1=request.form['add']
        contact1=request.form['contact']
        c=str(contact1)
        salary=request.form['salary']
        department=request.form['department']
        cur=db.connection.cursor()
        #cur.execute("SELECT * from employee_details where  or email='{}' or contact={}".format(email1,contact1))
        #account=cur.fetchone()
        #if account:
            #   msg="Duplicate Data Entry"
        


        
        if name1 == "":
                msg= "Please Enter Name"
        elif email1 == "":
            msg= "Please Enter Email"
        elif contact1 == "":
            msg= "Please Enter Contact"
        elif salary == "":
            msg= "Please Enter Salary"
        elif department == "":
            msg= "Please Enter Department"
        elif name1.isdigit()==True and regex.search(name1) != None:
            msg="Invalid Name"
        elif contact1== "":
            msg="Please fill contact"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email1): 
            msg = 'Invalid email address !'
        elif len(c)!=10:
            msg="Invalid contact"
        
        else:
            cur=db.connection.cursor()
            cur.execute("UPDATE employee_details set name='{}', email='{}' ,address='{}' ,contact='{}', salary={}, department='{}'  WHERE id1={}".format(name1, email1, address1,contact1,salary,department,id))
            db.connection.commit()
            return redirect(url_for('home'))

        id=request.args.get("id")
        cur=db.connection.cursor()
        cur.execute("SELECT * from employee_details WHERE id1={}".format(id))
        records=cur.fetchall() 
        return render_template("update_test.html", a=records, msg=msg)
            
        
    else:
        id=request.args.get("id")
        cur=db.connection.cursor()
        cur.execute("SELECT * from employee_details WHERE id1={}".format(id))
        records=cur.fetchall() 
        return render_template("update_test.html", a=records)
    return render_template ('emp_form.html')
        

   # except Exception as err:
        #return " Error while editing details. Please Try Again." 


        
@app.route('/deleteUser')
def deleteUser():
    try:

        db.connection=db.connect(host='localhost', user='root',password='',database='employee_details')
        id=request.args.get("id")
        cur=db.connection.cursor()
        cur.execute("Delete from employee_details where id1 = {}".format(id))
        db.connection.commit()
        return redirect(url_for('home'))
    

    except Exception as err:
        return "Err! Error while deleting details. Please Try Again." 


    

app.run(debug=True)
