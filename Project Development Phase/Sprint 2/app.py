from flask import *
from datetime import date
import ibm_db

app=Flask(__name__)
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;PROTOCOL=TCPIP;UID=mmv18931;PWD=Fk3vK5bxVH49RC3F", "", "")
print(conn)
print("Connecting Successful............")
retailer_id=0

@app.route("/", methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("Login/index.html",status="",colour="red")
    elif request.method=='POST':
        global retailer_id
        email=request.form["email"]
        password=request.form["password"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is not False):
            if(row['PASSWORD'] != password):
                return render_template("Login/index.html",status="Invalid Password",colour="red")
            else:
                temp='''select RETAILER_ID from retailers where email = \'{}\''''.format(email)
                exec_query = ibm_db.exec_immediate(conn, temp)
                dict= ibm_db.fetch_both(exec_query)
                retailer_id=dict["RETAILER_ID"]
                return render_template("Dashboard/index.html")

        return render_template("Login/index.html",status="Invalid Email",colour="red")

@app.route("/signup", methods=['GET','POST'])
def signup():
    
    if request.method=='GET':
        return render_template("Login/signup.html",status="",colour="red")
    elif request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        first_name=request.form["first_name"]
        last_name=request.form["last_name"]
        store_name=request.form["store_name"]
        address=request.form["address"]
        phone_number=request.form["phone_number"]
        query = '''select * from retailers where email = \'{}\''''.format(email)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into retailers(email, password, first_name, last_name, store_name, address, phone_number) values('{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(email, password, first_name, last_name, store_name, address, phone_number)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Login/signup.html",status="Signup Success",colour="green")
        else:
            return render_template("Login/signup.html",status="User Already Exists",colour="red")

@app.route("/dashboard", methods=['GET','POST'])
def dashboard():
    if request.method=="GET":
        return render_template("Dashboard/index.html")


@app.route("/add_customer", methods=['GET','POST'])
def add_customer():
    if request.method=="GET":
        return render_template("Dashboard/add_customer.html")
    elif request.method=="POST":
        name=request.form["name"]
        id=int(request.form["id"])
        query = '''select * from customer where customer_id = \'{}\''''.format(id)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into customer(customer_id,retailer_id,customer_name) values('{}', '{}', '{}')'''.format(id,retailer_id,name)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Dashboard/add_customer.html",status="Customer Added",colour="green")
        else:
            return render_template("Dashboard/add_customer.html",status="Customer Already Exists",colour="red")

@app.route("/view_customer", methods=['GET','POST'])
def view_customer():
    if request.method=="GET":
        query = '''select * from customer'''
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        name=[]
        id=[]
        while(row):
            name.append(row["CUSTOMER_NAME"])
            id.append(row["CUSTOMER_ID"])
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_customer.html",name=name,id=id,len=len(name))
        
@app.route("/add_item", methods=['GET','POST'])
def add_item():
    if request.method=="GET":
        return render_template("Dashboard/add_item.html")
    elif request.method=="POST":
        name=request.form["name"]
        price=float(request.form["price"])
        query = '''select * from items where item_name = \'{}\''''.format(name)
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        if(row is False):
            query = '''insert into items(retailer_id,item_name,price,left_out) values('{}', '{}', '{}', '{}')'''.format(retailer_id,name,price,0)
            exec_query = ibm_db.exec_immediate(conn, query)
            return render_template("Dashboard/add_item.html",status="Item Added",colour="green")
        else:
            return render_template("Dashboard/add_item.html",status="Item Already Exists",colour="red")

@app.route("/view_item", methods=['GET','POST'])
def view_item():
    if request.method=="GET":
        query = '''select * from items'''
        exec_query = ibm_db.exec_immediate(conn, query)
        row = ibm_db.fetch_both(exec_query)
        name=[]
        id=[]
        price=[]
        left_out=[]
        while(row):
            name.append(row["ITEM_NAME"])
            id.append(row["ITEM_ID"])
            price.append(row["PRICE"])
            left_out.append(row["LEFT_OUT"])
            row = ibm_db.fetch_both(exec_query)
        return render_template("Dashboard/view_item.html",name=name,id=id,price=price,left_out=left_out,len=len(name))

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)