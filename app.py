# Store this code in 'app.py' file
import os
import re
import MySQLdb.cursors

from os.path import join, dirname
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

app.secret_key = os.getenv('SEKEY')

app.config['MYSQL_HOST'] = os.getenv('DBHOST')
app.config['MYSQL_USER'] = os.getenv('DBUSER')
app.config['MYSQL_PASSWORD'] = os.getenv('DBPASS')
app.config['MYSQL_DB'] = os.getenv('DBNAME')

mysql = MySQL(app)

# Added by adam to test db connection and env variable
@app.route('/db_test')
def db_test():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    testquery = "select * from accounts where username = 'test'"
    cursor.execute(testquery)
    output = cursor.fetchall()
    return str(output)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query1 = "select * from accounts where username = '{un}' and password = '{pw}'".format(un=username, pw=password)
        cursor.execute(query1)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organization' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        organization = request.form['organization']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query2 = "select * from accounts where username = '{un}'".format(un=username)
        cursor.execute(query2)
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            query3 = "insert into accounts values (null, '{un}', '{pw}', '{em}', '{og}', '{addr}', '{cit}', '{st}', '{ct}', '{pc}')".format(un=username, pw=password, em=email, og=organization, addr=address, cit=city, st=state, ct=country, pc=postalcode)
            cursor.execute(query3)
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/index")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))


@app.route("/display")
def display():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query4 = "select * from accounts where id = '{idnum}'".format(idnum=session['id'])
        cursor.execute(query4)
        account = cursor.fetchone()
        return render_template("display.html", account=account)
    return redirect(url_for('login'))


@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'country' in request.form and 'postalcode' in request.form and 'organization' in request.form:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            organization = request.form['organization']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query5 = "select * from accounts where username = '{UN}'".format(UN=username)
            cursor.execute(query5)
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                query6 = "update accounts set username = '{un}', password = '{pw}', email = '{em}', organization = '{org}', address = '{addr}', city = '{cit}', state = '{st}', country = '{ct}', postalcode = '{pc}' where id='{idnum}'".format(un=username, pw=password, em=email, org=organization, addr=address, cit=city, st=state, ct=country, pc=postalcode, idnum=session['id'])
                cursor.execute(query6)
                mysql.connection.commit()
                msg = 'You have successfully updated !'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("update.html", msg=msg)
    return redirect(url_for('login'))


#if __name__ == "__main__":
#    app.run(host="localhost", port=int("5000"))
