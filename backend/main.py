from asyncio.windows_events import NULL
from enum import unique

from flask import Flask, json,redirect,render_template,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask.helpers import url_for
            

fid=0

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

class vehicle(db.Model):
    regno=db.Column(db.String(20),primary_key=True)
    state=db.Column(db.String(20))
    ownername=db.Column(db.String(30))
    rto=db.Column(db.String(20))
    pucnumber=db.Column(db.String(20),unique=True)
    insurancenumber=db.Column(db.String(20),unique=True)
    panno=db.Column(db.String(20))
    id=db.Column(db.Integer)

class insurance(db.Model):
    reg_no=db.Column(db.String(20))
    inc_no=db.Column(db.String(20),primary_key=True)
    inc_start=db.Column(db.String(20))
    exp_end=db.Column(db.String(20))
    get_from=db.Column(db.String(20))

class pollution(db.Model):
    reg_no=db.Column(db.String(20))
    puc_no=db.Column(db.String(20),primary_key=True)
    test_date=db.Column(db.String(20))
    valid_date=db.Column(db.String(20))
    tov=db.Column(db.String(20))
    vbd=db.Column(db.String(20))


@app.route("/")
def home():
    return render_template("index.html")




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
        db.engine.execute(f"INSERT INTO `register` (`username`,`email`,`phonenumber`,`age`,`password`) VALUES ('{username}','{email}','{phonenumber}','{age}','{encpassword}') ")
                
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
                global fid
                fid=user.id
                login_user(user)
                return render_template("index.html")
        except:
            flash("Invalid Credential","danger")
            return render_template("login.html") 
        else:
            flash(" Invalid Credentials","danger")
            return render_template("login.html") 
    return render_template("login.html")
        


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

@app.route('/addvehicle',methods=['POST','GET'])
@login_required
def addvehicle():
    if request.method=="POST":
        regno=request.form.get('regno')
        state=request.form.get('state')
        rto=request.form.get('rto')
        ownername=request.form.get('ownername')
        panno=request.form.get('panno')
        insurancenumber=request.form.get('insnumber')
        pucnumber=request.form.get('pucnumber')
        userinnum=vehicle.query.filter_by(insurancenumber=insurancenumber).first() 
        userpucnum=vehicle.query.filter_by(pucnumber=pucnumber).first()
        userregno=vehicle.query.filter_by(regno=regno).first()

        
        if userregno:
            flash("pollution id already registered","warning")
            return render_template("addvehicle.html")

        if userregno:
            flash("This register number already registered","warning")
            return render_template("addvehicle.html")  
        if userinnum:
            flash("This insurance number already registered","warning")
            return render_template("addvehicle.html")
        if userpucnum:
            flash("This pollution id already registered","warning")
            return render_template("addvehicle.html")

        global fid
        db.engine.execute(f"INSERT INTO `vehicle` (`regno`,`state`,`ownername`,`rto`,`pucnumber`,`insurancenumber`,`panno`,`id`) VALUES ('{regno}','{state}','{ownername}','{rto}','{pucnumber}','{insurancenumber}','{panno}','{fid}') ")
        puc_var=NULL
        ins_var=NULL
        puc=db.engine.execute(f"SELECT `puc_no` FROM `pollution` WHERE `reg_no`='{regno}'")
        ins=db.engine.execute(f"SELECT `inc_no` FROM `insurance` WHERE `reg_no`='{regno}'")
        print ("junaid4")
        for p in puc:
            puc_var=p[0]
        for i in ins:
            ins_var=i[0]
        if puc_var and ins_var:
            print(puc_var,ins_var)


        else: 
            db.engine.execute(f"DELETE from `vehicle` where `regno`='{regno}' ")
            flash("register number is invalid","warning")

        if puc_var and ins_var:
            if puc_var not in pucnumber:
                db.engine.execute(f"DELETE from `vehicle` where `regno`='{regno}' ")
                flash("invalid pollution certificate id for register number="+regno,"warning")
            if ins_var not in insurancenumber:
                db.engine.execute(f"DELETE from `vehicle` where `regno`='{regno}' ")
                flash("invalid insurance number for register number="+regno,"warning")
            elif(puc_var in pucnumber and  ins_var in insurancenumber) :
                flash("vehicle details successfully verified","success")
                

           


        
        return render_template("addvehicle.html")

    return render_template("addvehicle.html")





app.run(debug = True)



