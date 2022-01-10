from enum import unique

from flask import Flask, json,redirect,render_template,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from werkzeug.security import generate_password_hash,check_password_hash

            

#mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="madhujunaid"

#for unique access
login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(id):
    return register.query.get(int(id))


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/register")
# def register():
#     return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/register',methods=['POST','GET'])
def register():
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
        if user or useremail or phno:
            flash("Email or username or phno is already taken","warning")
            return render_template("register.html")
        if password!=checkpassword:
            flash("reentered password wrong")
            return render_template("register.html")
        if int(age)<=int(18):
            flash("reentered password wrong")
            return render_template("register.html")
        if len(password)<8:
            flash("enter minimum 8 characters of password")
            return render_template("register.html")
        encpassword=generate_password_hash(password)
        new_user=db.engine.execute(f"INSERT INTO `register` (`username`,`email`,`phonenumber`,`age`,`password`) VALUES ('{username}','{email}','{phonenumber}','{age}','{encpassword}') ")
                
        flash("register Success Please Login","success")
        return render_template("login.html")

    return render_template("register.html")

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/autoease'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))

class register(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15),unique=True)
    email=db.Column(db.String(30),unique=True)
    phonenumber=db.Column(db.BigInteger,unique=True)
    password=db.Column(db.String(100))
    age=db.Column(db.Integer)


@app.route("/test")
def test():
    try:
        a=Test.query.all()
        print(a)
        return('connected')
    except Exception as e:
        print(e)
        return f'not{e}'   




app.run(debug = True)



