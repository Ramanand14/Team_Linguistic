import os
from flask import Flask, request, render_template, redirect,send_file
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

#Required libraries to use sqlite database
import sqlite3
from sqlite3 import Error


d = enchant.Dict("en_US")

UPLOAD_FOLDER = os.path.dirname('__file__')

app = Flask(__name__, template_folder = 'template/HTML')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "abcd"

text1 = []
text2 = []
file_content = ""
filename = ""
result = ''

@app.route("/", methods=['GET','POST']) 
def main_page():
    return render_template("main_page.html")

@app.route("/radio_check", methods=['GET', 'POST'])
def radio_check():
    if request.method == 'POST':
        option1 = request.form.get('radiobtn')
        if option1 == '1':
            a = keyboard_ip()
            print(a)
        elif option1 == '2':
            a = request.form['VText']
            print(a)
        elif option1 == '3':
            a = file_ip()
            print(a)
            return render_template("main_page.html", etext=a)
    return render_template("main_page.html")

@app.route("/help_page", methods=['GET','POST']) 
def help_page():
    return render_template("help_page.html")

def keyboard_ip():
    if request.method == 'POST':
        user_ip = request.form['hinglish']
        print("\n***********I/P text***************")
        print(user_ip)
        text = conversion_fun(user_ip)
        #print("Inside keyboard_ip function text: ", text)
    return text

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

#Define connection function which will connect to database 
def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("Database Opening Error!!!")
    return conn

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

def first(rtext):
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
                #If there exist such match of username and password, kindly open mainpage of web application ['kaise', 'ho', 'talk', 'to', 'you', 'later']
                rtext = str(row[1])
                #print(rtext, ": is available")
                text1.append(rtext)
    except Error as e:
        print("Fail")     

def conversion_fun(input_txt):
    global result
    global text1
    global text2
    result = ""
    text1 = ""
    text2 = ""
    token = word_tokenize(input_txt)
    #print("\n***********Shortnotations available status***************")
    for i in token:
        #print(i, "-> passing to database")
        first(i)

    ft = " ".join(text1)
    #print("***********Shortnotations removed text**************")
    #print(ft)

    token = word_tokenize(ft)

    #print("\n**************Identify English words******************")
    for i in token:
        if(d.check(i) == True):
            res = EngtoHindi(i)
            text2.append(res.convert)
            #print(i, ": ", text2)
        else:
            #print(i)
            text2.append(i)

    #print("\n**************list items*********************")
    #print(text2)

    #ft = listToString(text)
    print("**************Convert list -> sentence***********")
    ft = " ".join(text2)
    print(ft)

    #result = transliterate(master, sanscript.ITRANS, sanscript.DEVANAGARI)
    result = transliterate(ft, sanscript.ITRANS, sanscript.DEVANAGARI)
    #print("\n*****************Final result********************")
    #print(result)

    a = perform_operation()
    #return result
    return a

if __name__=="__main__":
    app.run(debug=True)#running our app