from enum import unique

from flask import Flask, json,redirect,render_template,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask.helpers import url_for
            

#mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="madhujunaid"

#for unique access
login_manager=LoginManager(app)
login_manager.login_view='login'

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/autoease'
db=SQLAlchemy(app)

@login_manager.user_loader
def load_user(id):
    return register.query.get(int(id))

class register(UserMixin, db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(30),unique=True)
    phonenumber=db.Column(db.BigInteger,unique=True)
    password=db.Column(db.String(1000))
    age=db.Column(db.Integer)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/addvehicle")
def addvehicle():
    return render_template("addvehicle.html")

# @app.route("/login")
# def login():
#     return render_template("login.html")

@app.route('/register',methods=['POST','GET'])
def registers():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('email')
        phonenumber=request.form.get('phno')
        age=request.form.get('age')
        password=request.form.get('password')
        checkpassword=request.form.get('chpassword')
        print(username,email,phonenumber,age,password,checkpassword)
        user=register.query.filter_by(username=username).first()
        useremail=register.query.filter_by(email=email).first()
        phno=register.query.filter_by(phonenumber=phonenumber).first()
        if user :
            flash("Username is already taken","warning")
            return render_template("register.html")
        if  useremail :
            flash("Emailid is already taken","warning")
            return render_template("register.html")
        if phno:
            flash("phno is already taken","warning")
            return render_template("register.html")     
        if password!=checkpassword :
            flash("Entered password do not match","warning")
            return render_template("register.html")
        if int(age)<=int(18):
            flash("Age Restriction","warning")
            return render_template("register.html")
        if len(password)<8:
            flash("enter minimum 8 characters of password","warning")
            return render_template("register.html")
        encpassword=generate_password_hash(password)
        new_user=db.engine.execute(f"INSERT INTO `register` (`username`,`email`,`phonenumber`,`age`,`password`) VALUES ('{username}','{email}','{phonenumber}','{age}','{encpassword}') ")
                
        flash("Registered,Please Login","success")
        return render_template("login.html")

    return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        user=register.query.filter_by(username=username).first()
        try:
            if user and check_password_hash(user.password,password):
                login_user(user)
                return render_template("index.html")
        except:
            flash("Invalid Credential","danger")
            return render_template("login.html") 

        else:
            flash("Invalid Credentials","danger")
            return render_template("login.html") 
    return render_template("login.html")
        
        

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))







app.run(debug = True)



