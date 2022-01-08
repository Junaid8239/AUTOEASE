from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy

#mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="madhujunaid"

@app.route("/")
def home():
    return render_template("index.html")

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/autoease'
db=SQLAlchemy(app)

class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))



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



