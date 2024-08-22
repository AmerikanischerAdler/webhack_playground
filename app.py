#!/opt/homebrew/bin/python3.11

import requests
import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
my_pw = os.environ["MYSQLPW"]

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{my_pw}@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


# Insecure
@app.route('/xss-me', methods=['GET', 'POST'])
def xss_me():
    user_input = ''
    if request.method == 'POST':
        user_input = request.form.get('xss_input', '')
    return render_template('xss_me.html', user_input=user_input)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        query_stmt = f"SELECT user_id, username FROM users WHERE username='{username}' AND password='{password}'"

        with db.engine.begin() as conn:
            result = conn.execute(text(query_stmt))
            conn.commit()
        user = result.fetchone()

        if user:
            message = f"Welcome, {username}!"
            #comment out for XSS and SQl injection testing
            return redirect(url_for('welcome', user_id=user[0])) 
        else:
            message = "Incorrect Username or Password."

    return render_template('login.html', message=message)

@app.route('/welcome/<int:user_id>', methods=['GET'])
def welcome(user_id):
    query_stmt = f"SELECT username FROM users WHERE user_id={user_id}"
    with db.engine.begin() as conn:
        result = conn.execute(text(query_stmt))
        conn.commit()
    user = result.fetchone()

    if user:
        return f"Welcome, {user[0]}! You are logged in."
    else:
        return "User not found!"



# Secure 
bad_chars = ["'", ";", "--", "#"]

def blacklist(uname):
    for char in bad_chars:
        if char in uname.lower():
            return True
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if blacklist(username):
            message = "No Hacking"
            return render_template('register.html', message=message)

        check_query = "SELECT username FROM users WHERE username=:username"
        with db.engine.begin() as conn:
            user_exists = conn.execute(text(check_query), {'username': username}).fetchone()
            conn.commit()

        if user_exists:
            message = "User already exists!"
        else:
            insert_query = "INSERT INTO users (username, password) VALUES (:username, :password)"
            with db.engine.begin() as conn:
                conn.execute(text(insert_query), {'username': username, 'password': password})
                conn.commit()

            message = "Registration successful!"

    return render_template('register.html', message=message)


# Open Redirect Vulnerability
@app.route('/redirect', methods=['GET'])
def redirect_func():
    return render_template('redirect.html')

@app.route('/open', methods=['GET'])
def open():
    target_url = request.args.get('url')
    action = request.args.get('action', 'redirect')

    # open redirection 
    if action == 'redirect':
        return redirect(target_url)

    # SSRF
    elif action == 'fetch':
        try:
            response = requests.get(target_url, timeout=5)
            if response.status_code == 200:
                return f"Received 200 ok {target_url}"
            else:
                return f"Received {response.status_code} from {target_url}"

        except requests.ConnectionError:
            return f"Connection Refused by {target_url}"
        except requests.Timeout:
            return f"Connection timed out for {target_url}"
        except Exception as e:
            return str(e)

    return "specify action and url parameters"


# HTML in python using flask
#@app.route('/Users/americaneagle1776/Documents/intentional_growth/programming/language/webdev/python/flask/')
#def hello_world():
#    return '<h1 style="text-align: center;">Hello World!</h1>'\
#            '<p>This is a paragraph!</p>'

# Change output base on path input (numbers)
#@app.route('/Users/americaneagle1776/Documents/intentional_growth/programming/language/webdev/python/flask/file/<int:number>/')
#def bye(number):
#    return f'This is page {number}'

# Change output base on path input (names)
#@app.route('/Users/americaneagle1776/Documents/intentional_growth/programming/language/webdev/python/flask/title/<name>/')
#def new(name):
#    return f'Welcome {name}'

if __name__ == '__main__':
    app.run(debug=True)

