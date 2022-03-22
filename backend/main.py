from asyncio.windows_events import NULL
from enum import unique


from flask import Flask, json,redirect,render_template,flash,request,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import login_required,logout_user,login_user,login_manager,LoginManager,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from flask.helpers import url_for
from fpdf import FPDF     

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

class autocard(db.Model):
    acard_id=db.Column(db.Integer,primary_key=True)
    auid=db.Column(db.Integer)
    astate=db.Column(db.String(20))
    atov=db.Column(db.String(20))
    avbd=db.Column(db.String(20))
    aownername=db.Column(db.String(20))
    arto=db.Column(db.String(20))
    areg_no=db.Column(db.String(20))
    apan_no=db.Column(db.String(20))
    apuc_no=db.Column(db.String(20),primary_key=True)
    apuc_testdate=db.Column(db.String(20))
    apuc_validdate=db.Column(db.String(20))
    ains_no=db.Column(db.String(20),primary_key=True)
    ains_startdate=db.Column(db.String(20))
    ains_enddate=db.Column(db.String(20))





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
                pucdetails=db.engine.execute(f"SELECT * FROM `pollution` WHERE `reg_no`='{regno}'")
                for p in pucdetails:
                    puctest_var=p[2]
                    pucvalid_var=p[3]
                    tov_var=p[4]
                    vbd_var=p[5]

                insdetails=db.engine.execute(f"SELECT * FROM `insurance` WHERE `reg_no`='{regno}'")
                for i in insdetails:
                    insstart_var=i[2]
                    insend_var=i[3]


                db.engine.execute(f"insert into `autocard` (`auid`,`astate`,`atov`,`avbd`,`aownername`,`arto`,`areg_no`,`apan_no`,`apuc_no`,`apuc_testdate`,`apuc_validdate`,`ains_no`,`ains_startdate`,`ains_enddate`) values ('{fid}','{state}','{tov_var}','{vbd_var}','{ownername}','{rto}','{regno}','{panno}','{puc_var}','{puctest_var}','{pucvalid_var}','{ins_var}','{insstart_var}','{insend_var}')")
                flash("vehicle details successfully verified","success")


        
        return render_template("addvehicle.html")

    return render_template("addvehicle.html")


@app.route('/vdata/', defaults={'reg' : 'none'},methods=['POST','GET'])
@login_required
def vdata(reg):
    reg = request.args.get('reg')
    print(reg)        
    id=current_user.id
    print (id)
    m=id
    postdata=autocard.query.filter_by(auid=m).all()
    return render_template("vdata.html",postdata=postdata,id=id,reg=reg)

@app.route('/dvehicle/<string:reg_no>',methods=['POST','GET'])
@login_required
def dvehicle(reg_no):
    db.engine.execute(f"delete from `vehicle` where `regno`='{reg_no}'")
    db.engine.execute(f"delete from `autocard` where `areg_no`='{reg_no}'")
    flash("vehicle deleted","danger")
    id=current_user.id
    m=id
    postdata=autocard.query.filter_by(auid=m).all()
    return render_template("vdata.html",postdata=postdata,regno=reg_no,areg_no=reg_no)
    #return redirect("vdata.html")
    


@app.route('/download/report/pdf')  
def download_report():
        id=current_user.id
        m=id
        postdata=autocard.query.filter_by(auid=m).all()
      
        for i in postdata:
                card=i.acard_id
                owner=i.aownername
                puc=i.apuc_no
                ins=i.ains_no
                reg=i.areg_no
                insend=i.ains_enddate
                pucend=i.apuc_validdate
        
        class PDF(FPDF):
            def header(self):
                self.set_draw_color(0,0,0)
                self.set_fill_color(52, 235, 131)
                self.set_text_color(255,255,255)
                self.set_line_width(1.5)
                self.set_font('helvetica','B',14.0) 
                self.set_x(80)
                self.cell(40, 10, 'AUTOEASE', align='C',border=1,fill=1)
                self.ln(30)
               
            def footer(self):
                self.set_y(-155)
                self.set_font('helvetica','I',10)
                self.cell(0,10,f'Thank you for using AUTOEASE... :D',align='L')
                self.cell(0,10,f'Page{self.page_no()}/{{nb}}',align='C')
            def body(self):
                self.set_x(60)
                w=80
                h=8
                self.set_fill_color(235, 244, 245)
                self.cell(80,10,f'AUTOCARD',align='C',fill=1,ln=1,border=1)
                self.set_draw_color(0,0,0)
                self.set_fill_color(194, 171, 219)
                
                self.set_x(60)
                self.cell(w,h,f'card_id : {str(card)}', border=1,ln=True,fill=1) 
                self.set_x(60)
                pdf.cell(w,h,f'Registration id : {str(reg)}', border=1,ln=True,fill=1)
                self.set_x(60)
                pdf.cell(w,h, f'owner : {str(owner)}', border=1,ln=True,fill=1)
                self.set_x(60)
                pdf.cell(w,h, f'pollution_id : {str(puc)}', border=1,ln=True,fill=1)
                self.set_x(60)
                pdf.cell(w,h,f'valid date : {str(pucend)}', border=1,ln=True,fill=1)
                self.set_x(60)
                pdf.cell(w,h, f'insurance id : {str(ins)}', border=1,ln=True,fill=1)
                self.set_x(60)
                pdf.cell(w,h,f'valid date : {str(insend)}', border=1,ln=True,fill=1)
        pdf = PDF('p','mm','Letter')
        pdf.add_page()
        pdf.alias_nb_pages
        pdf.body()
        pdf.ln(40)
        return Response(pdf.output(dest='S'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=employee_report.pdf'})

app.run(debug = True)



