#required libraries
import os
from flask import Flask, request, render_template, redirect
from werkzeug.utils import secure_filename

from nltk import text
import idiomcorpus
import nltk
nltk.download('punkt')
from mtranslate import translate
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from nltk.tokenize import word_tokenize
from englisttohindi.englisttohindi import EngtoHindi
import enchant

import sqlite3
from sqlite3 import Error

d = enchant.Dict("en_US")

UPLOAD_FOLDER = os.path.dirname('__file__')
#initialize the flask application
app = Flask(__name__, template_folder = 'template/HTML')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "LinguisTic05"

#global variables
text1 = []
text2 = []
file_content = ""
filename = ""
result = ''

#root page of the application
@app.route("/", methods=['GET','POST']) 
def home_page():
    return render_template("home_page.html")

#check for the input method 
@app.route("/radio_check", methods=['GET', 'POST'])
def radio_check():
    global result
    global text1
    global text2 
    if request.method == 'POST':
        option1 = request.form.get('radiobtn')
        if option1 == '1':
            a = keyboard_ip()
        elif option1 == '2':
            t = request.form['text3']
            a = conversion_fun(t)
        elif option1 == '3':
            a = file_ip()
        else:
            t = request.form['vir_text']
            a = conversion_fun(t)
        text1 = []
        text2 = []
        return render_template("home_page.html", etext=a)
    return render_template("home_page.html")

#open help page
@app.route("/help_page", methods=['GET','POST']) 
def help_page():
    return render_template("help_page.html")

#take input through keyboard
def keyboard_ip():
    if request.method == 'POST':
        user_ip = request.form['hinglish']
        text = conversion_fun(user_ip)
    return text

#take file as input from the user
def file_ip():
    global file_content
    global filename
    file_content = ""
    filename = ""
    if request.method == 'POST':
        # check if the post request has the file part
        if 'myfile' not in request.files:
            return redirect(request.url)
        file = request.files['myfile']
        # if user does not select file, browser also submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Read File
            with open(os.path.join(app.config['UPLOAD_FOLDER'],filename)) as f:
                file_content=str(f.read())
            text = conversion_fun(file_content)            
    return text

#define connection function which will connect to database 
def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("Database Opening Error!!!")
    return conn

#call perform_operation to convert the text to english
def perform_operation():
    global result
    object=idiomcorpus.Idiomcorpus()
    object.idiom_init(result)

    try:
        object.check_idiom()
        object.idiom_convert()
        b = object.idiom_display()
        return b
    except:
         print(" ")

#check for short notations availability in text
def shortnot(rtext):
    global text1
    try:
        database = r"Database.db"
        conn = connection(database)
        with conn:
            Short_Notations = rtext
            rows=0
            cur = conn.cursor()
            cur.execute("Select * from Keys where Short_Notations = ?",(Short_Notations,))
            rows = cur.fetchall()
            if len(rows) == 0:
                text1.append(rtext)
            for row in rows:
                rtext = str(row[1])
                text1.append(rtext)
    except Error as e:
        print("Fail")     

#call conversion_fun to convert the text to complete hindi
def conversion_fun(input_txt):
    global result
    global text1
    global text2
    token = word_tokenize(input_txt)
    for i in token:
        shortnot(i)

    ft = " ".join(text1)

    token = word_tokenize(ft)

    for i in token:
        if(d.check(i) == True):
            res = EngtoHindi(i)
            text2.append(res.convert)
        else:
            text2.append(i)

    ft = " ".join(text2)

    result = transliterate(ft, sanscript.ITRANS, sanscript.DEVANAGARI)
    a = perform_operation()
    return a

if __name__=="__main__":
    app.run(debug=True)#running our app