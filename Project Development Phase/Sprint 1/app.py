from turtle import st
from flask import Flask, render_template, request, redirect, url_for, session
from markupsafe import escape

import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=54a2f15b-5c0f-46df-8954-7e38e612c2bd.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32733;SECURITY=SSL;PROTOCOL=TCPIP;UID=rrr78482;PWD=USdGthdthovmVWAn", "", "")
print(conn)
print("Connecting Successful............")


app=Flask(__name__,template_folder="templates",static_folder="static")

app.config['DEBUG'] = True


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
  if request.method == 'POST':

    name = request.form['registerFullName']
    username = request.form['registerUsername']
    password = request.form['registerPassword1']
    repass = request.form['registerPassword2']

    print(name)

    sql = "SELECT * FROM Retailer WHERE name =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,name)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('signup.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO Retailer VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, name)
      ibm_db.bind_param(prep_stmt, 2, username)
      ibm_db.bind_param(prep_stmt, 3, password)
      ibm_db.bind_param(prep_stmt, 4, repass)
      ibm_db.execute(prep_stmt)
    
    return render_template("home.html", msg="Retailer Login successfuly..")


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/home")
def hello():
    return render_template("home.html")

@app.route("/about")
def profile():
    return render_template("about.html")


@app.route("/signin")
def signin():
    return render_template("signin.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
