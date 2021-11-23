from flask import Flask, render_template,request
import speech_recognition as sr
from gtts import gTTS
import os
from time import sleep
import pyglet

app=Flask(__name__, template_folder='template')

@app.route('/')
def home():
	return render_template('input_suhana.html')

@app.route('/output',methods=['POST','GET'])
def result():
    transcript=""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        transcript = r.recognize_google(audio)
        #print(transcript)
    return render_template('input_suhana.html',transcript = transcript)

@app.route('/submit',methods=["POST","GET"])
def submit():
	input=request.form.get('result')
	print(input)
	language = 'en'
	speech = gTTS(text=input,lang=language,slow=False)
	speech.save('out.mp3')
	music = pyglet.media.load('out.mp3',streaming=False)
	music.play()
	os.remove('out.mp3')
	return render_template('input_suhana.html',transcript=input)
	
@app.route('/sub',methods=["POST","GET"])	
def sub():
	print(1)
	input1=request.form.get('Eng')
	print(input1)
	language = 'en'
	speech = gTTS(text=input1,lang=language,slow=False)
	speech.save('ot.mp3')
	music = pyglet.media.load('ot.mp3',streaming=False)
	music.play()
	os.remove('ot.mp3')
	return render_template('input_suhana.html',transcript1=input1)

if __name__== '__main__':
    app.run(debug=True)


