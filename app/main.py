import os
import pickle
from datetime import datetime

import pandas as pd
from flask import Flask, flash, render_template, request

app = Flask(__name__)


icon = {
    'folder': 'folder',
    '.jpg': "file-image",
    '.pdf': "file-earmark-richtext",
    '.html': "file-richtext",
    '.ppt': '',
    '.xls': '',
    '.text': "file-earmark-text",
    '.doc': 'file-earmark-font',
    'no-icon': "file-x"
}


test = [{'file': 'some file', 'topic_x': 'hello',
         'absolute_path': '../data/t5/000002.doc', 'extension': '.html'}]


@ app.route('/', methods=['POST'])
def open_file():
    filepath = request.form.get('filepath')
    os.popen(f"open {filepath}")

    # return render_template('index.html', rows_len=len(test), rows=test, icon=icon)
    return '', 204


@ app.route('/<name>')
def index(name, rows=test):
    name = name.capitalize()

    return render_template('index.html', name=name, rows_len=len(test), rows=test, icon=icon)


@ app.route('/home')
def homepage():
    current_folder = os.getcwd()
    breadcrumbs = current_folder[1:].split('/')
    files = os.listdir(current_folder)
    no_files = len(files)

    return render_template('homepage.html', breadcrumbs=breadcrumbs, nfiles=no_files, files=files)


@ app.route('/browser')
def index2():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


if __name__ == '__main__':
    app.run(debug=True)
