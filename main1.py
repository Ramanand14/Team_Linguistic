# main.py / Idiom Corpus
# Gourav Siddhad
# 07-04-2018

import idiomcorpus
from mtranslate import translate
from tkinter import *


def perform_operation():
    object = idiomcorpus.Idiomcorpus()
    object.idiom_init(e1.get())    
    e4.delete(0, END)

    try:
        object.check_idiom()
        object.idiom_convert()
        object.idiom_display()
        
        e4.insert(0, object.output)
    except:
       
        e4.insert(0, translate(e1.get(), 'en'))


master = Tk()
master.title("Hindi to English")
width, height = 800, 200
xcord = master.winfo_screenwidth()/2 - width/2
ycord = master.winfo_screenheight()/2 - height/2
master.geometry("%dx%d+%d+%d" % (width, height, xcord, ycord))

Label(master, text="Hindi").place(x=width/12,
                                  y=height/10, width=width/6, height=2*height/15)
Label(master, text="English").place(x=width/12, y=5 *
                                    height/10, width=width/6, height=2*height/15)

e1 = Entry(master, justify='center')
e1.place(x=width/4, y=height/10, width=4*width/6, height=2*height/15)
e1.insert(END, "﻿क्या आप उन्हें मदद कर सकते हैं")

e4 = Entry(master, justify='center')
e4.place(x=width/4, y=5*height/10, width=4*width/6, height=2*height/15)

Button(master, text='Quit', command=master.quit).place(
    x=width/8, y=7*height/10, width=width/4, height=height/5)
Button(master, text='Convert', command=perform_operation).place(
    x=5*width/8, y=7*height/10, width=width/4, height=height/5)

mainloop()
