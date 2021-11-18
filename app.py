from flask import Flask, request, render_template

#Required libraries to use sqlite database
import sqlite3
from sqlite3 import Error

app = Flask(__name__, template_folder = 'template/HTML')

app.secret_key = "abcd"

@app.route("/", methods=['GET','POST']) 
def main_page():
    return render_template("main_page.html")

@app.route("/radio_check", methods=['GET', 'POST'])
def radio_check():
    if request.method == 'POST':
        option1 = request.form.get('radiobtn')
        if option1 == '1':
            keyboard_ip()
        elif option1 == '2':
            print("inside 2")
        elif option1 == '3':
            print("inside 3")
    return render_template("main_page.html")

@app.route("/clear_btn", methods=['GET','POST']) 
def clear_btn():
    return render_template("main_page.html")

@app.route("/admin_page", methods=['GET','POST'])
def admin_page():
    database = r"Database.db"
    conn = connection(database)
    if request.method == 'POST':
        command = request.form['command']
        print(command)
        if command == 'Sign In':
            sign_in()
        elif command == 'Sign Up':
            sign_up()
    return render_template("admin_page.html")

def keyboard_ip():
    print("key")
    if request.method == 'POST':
        user_ip = request.form['hinglish']
        print(user_ip)
    return render_template("main_page.html")

def voice_ip():
    return render_template("main_page.html")

def file_ip():
    return render_template("main_page.html")

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    return render_template("admin_page.html")

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    return render_template("admin_page.html")

#Define connection function which will connect to database 
def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("Database Opening Error!!!")
    return conn

if __name__=="__main__":
    app.run(debug=True)#running our app