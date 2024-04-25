from flask import Flask, render_template,redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "santhoshi"
app.config["MYSQL_DB"] = "customer"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"


mysql = MySQL(app)




@app.route("/deleteUser/<string:id>", methods=["GET", "POST"])
def deleteUser(id):
    con = mysql.connection.cursor()
    
    print(id)
    sql = "delete from user where id=%s"
    con.execute(sql, [id])
    mysql.connection.commit()
    con.close()
    return redirect(url_for("home"))
    


@app.route("/editUser/<string:id>", methods=["GET", "POST"])
def editUser(id):
    con = mysql.connection.cursor()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["gender"]
        city = request.form["city"]
        sql = "update user set NAME=%s, AGE=%s, GENDER=%s, CITY=%s where id=%s"
        con.execute(sql, [name, age, gender, city, id])
        mysql.connection.commit()
        con.close()
        print("updated")
        return redirect(url_for("home"))
    sql = "select * from user where id=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    mysql.connection.commit()
    con.close()
    print(res)
    return render_template("editUser.html", data=res)


@app.route("/addUser", methods=["GET","POST"])
def addUser():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        city = request.form['city']
        con = mysql.connection.cursor()
        sql = "insert into user (NAME, AGE, GENDER, CITY) values(%s, %s, %s, %s)"
        con.execute(sql, [name, age, gender, city])
        mysql.connection.commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("addUser.html")




@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "select * from user"
    con.execute(sql)
    res = con.fetchall()
    print(res)
    return render_template("home.html", datas=res)





if(__name__ == '__main__'):
    app.run(debug=True)
