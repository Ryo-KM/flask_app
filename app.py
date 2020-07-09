import sys
import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from datetime import datetime

UPLOAD_FOLDER = '/Users/ryo/Gs_project/python_vscode/output_data'
OUTPUT_FILE = 'output.csv'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv', 'xlsx']

# appという名前でflaskのインスタンスを作成
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'dev_16'

def process_file(input_file_path):
  ### 実際に処理を行う関数 ###
  output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], OUTPUT_FILE)
  with open(output_file_path, 'w') as f:
      f.write('A, B, C')

def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_file_path)
        
        process_file(input_file_path)
        
        return redirect(url_for('processed_file', filename=OUTPUT_FILE))
  return render_template('index.html')
  
@app.route('/uploads/<filename>')
def processed_file(filename):
  output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/<name>/<number>')
def login(name, number):
  return render_template('login.html', name=name, number=number)

@app.route('/userlist')
def user_list():
  users = [
    'Taro', 'Jiro', 'Saburo', 'Shiro', 'Hanako'
  ]
  return render_template('userlist.html', users=users)


if __name__ == '__main__':
  app.run(debug=True)