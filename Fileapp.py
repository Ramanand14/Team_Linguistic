import os
from flask import Flask, flash,redirect,send_file, render_template, request
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.dirname('__file__')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

file_content = ""
filename = ""

@app.route("/", methods=['GET','POST']) 
def main_page():
    return render_template("main_page.html")

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    global file_content
    global filename
    if request.method == 'POST':
        # check if the post request has the file part
        if 'myfile' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['myfile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Read File
            with open(os.path.join(app.config['UPLOAD_FOLDER'],filename)) as f:
                file_content=str(f.read())
            print("saved file successfully")
            
    return render_template('main_page.html',file_content=file_content)

@app.route('/download_btn', methods=['GET', 'POST'])
def download_btn():
    global filename
    print("here1")
    if request.method == 'GET':
        print("here")
        file_path = UPLOAD_FOLDER + filename
        print("there")
        return send_file(file_path, as_attachment=True)
    print("end")

if __name__==('__main__'):
    app.run(debug=True)
