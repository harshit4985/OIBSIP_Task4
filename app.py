import sqlite3
from flask import Flask,render_template,request, jsonify
app=Flask(__name__)
@app.route('/')
def index() :
    return render_template("login_signup.html")

@app.route('/reg1',methods=["POST", "GET"])
def reg1() :
    if request.method=="POST" :
        name=request.form["name"]
        email=request.form["email"]
        phone=request.form["phone"]
        password=request.form["password"]
        con=sqlite3.connect("database.db")
        cr=con.cursor()
        cr.execute("create table if not exists std(name TEXT,email TEXT,phone TEXT,password TEXT)")
        cr.execute("insert into std values(?,?,?,?)",[name,email,phone,password])
        con.commit()
        return render_template("login_signup.html")
    return render_template("login_signup.html")
@app.route('/log1',methods=["POST", "GET"])
def log1() :
    if request.method=="POST" :
        email=request.form["email"]
        password=request.form["password"]
        con=sqlite3.connect("database.db")
        cr=con.cursor()
        cr.execute("select * from std where email='"+email+"' and password='"+password+"'")
        result=cr.fetchall()
        if result :
            cr.execute("select * from std")
            result1=cr.fetchall()
            return render_template("userlog.html", result1=result1)
        else:
            return render_template("login_signup.html")
    return render_template("login_signup.html")
@app.route('/remove/<Id>')
def remove(Id) :
    print(Id)
    con=sqlite3.connect("database.db")
    cr=con.cursor()
    cr.execute("delete from std where phone = '"+Id+"'")
    con.commit()

    cr.execute("select * from std")
    result1=cr.fetchall()
    return render_template("userlog.html", result1=result1)

@app.route('/update/<Id>')
def update(Id) :
    print(Id)
    con=sqlite3.connect("database.db")
    cr=con.cursor()
    cr.execute("select * from std where phone = '"+Id+"'")
    result2=cr.fetchone()
    print(result2)
    return render_template("update.html", result2=result2)

@app.route('/update_info',methods=["POST", "GET"])
def update_info():
    if request.method=="POST" :
        name=request.form["name"]
        email=request.form["email"]
        phone=request.form["phone"]
        password=request.form["password"]
        con=sqlite3.connect("database.db")
        cr=con.cursor()
        cr.execute("update std set name='"+name+"',email='"+email+"',password='"+password+"' where phone='"+phone+"'")
        con.commit()

        cr.execute("select * from std")
        result1=cr.fetchall()
        return render_template('userlog.html', result1=result1)

@app.route('/change_password',methods=["POST", "GET"])
def change_password():
     if request.method=="POST" :
        email=request.form["email1"]
        con=sqlite3.connect("database.db")
        cr=con.cursor()
        cr.execute("select * from std where email='"+email+"'")
        result = cr.fetchall()
        print(result)
        if result:
            msg="yes"
        else:
            msg="no"
        return render_template("login_signup.html")

@app.route('/new_password',methods=["POST","GET"])
def new_password():
    if request.method=="POST" :
        email=request.form["email1"]
        new_password=request.form["new_password"]
        con=sqlite3.connect("database.db")
        cr=con.cursor()
        cr.execute("update std set password='"+new_password+"' where email='"+email+"'")
        result = cr.fetchall()
        con.commit()
        if result:
            cr.execute("select * from std")
            result1=cr.fetchall()
            return render_template("userlog.html", result=result)
        else:
            return render_template("login_signup.html")

if __name__=="__main__":
    app.run(debug=True)
