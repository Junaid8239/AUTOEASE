from flask import Flask,redirect,render_template

#mydatabase connection
local_server=True
app=Flask(__name__)
app.secret_key="madhujunaid"

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
   app.run(debug = True)



