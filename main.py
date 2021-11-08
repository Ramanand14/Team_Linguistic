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

def perform_operation():
    object=idiomcorpus.Idiomcorpus()
    object.idiom_init(result)

    try:
        object.check_idiom()
        object.idiom_convert()
        object.idiom_display()

    except:
         print(" ")

#Define connection function which will connect to database 
def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("Database opening error")
    return conn

def first(rtext):
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
                text.append(rtext)
            for row in rows:
                #If there exist such match of username and password, kindly open mainpage of web application
                rtext = str(row[1])
                print(rtext, ": is available")
                text.append(rtext)
    except Error as e:
        print("Fail")     

master=input("Enter Hinglish text:")
print("\n***********I/P text***************")
print(master)

text = []
text1 = []
token = word_tokenize(master)

print("\n***********Shortnotations available status***************")
for i in token:
    print(i, "-> passing to database")
    first(i)

ft = " ".join(text)
print("***********Shortnotations removed text**************")
print(ft)

token = word_tokenize(ft)

print("\n**************Identify English words******************")
for i in token:
    if(d.check(i) == True):
        res = EngtoHindi(i)
        text1.append(res.convert)
        print(i, ": ", text1)
    else:
        print(i)
        text1.append(i)

print("\n**************list items*********************")
print(text1)


#ft = listToString(text)
print("**************Convert list -> sentence***********")
ft = " ".join(text1)
print(ft)

#result = transliterate(master, sanscript.ITRANS, sanscript.DEVANAGARI)
result = transliterate(ft, sanscript.ITRANS, sanscript.DEVANAGARI)
print("\n*****************Final result********************")
print(result)

a = perform_operation()
