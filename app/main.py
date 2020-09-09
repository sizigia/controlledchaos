import os
import pickle
import re
from datetime import datetime

import pandas as pd
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from helpers import blind_categories, get_attributes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mockupkey'


icon = {
    'folder': 'folder',
    '.jpg': "file-image",
    '.pdf': "file-earmark-richtext",
    '.html': "file-post",
    '.ppt': 'file-slides',
    '.xls': 'file-spreadsheet',
    '.text': "file-earmark-text",
    '.doc': 'file-earmark-font',
    'no-icon': "file-x"
}

formats = {
    'audio_vid': ['.aif', '.cda', '.mid', '.midi', '.mp3', '.m4a', '.mpa', '.ogg', '.wav', '.wma', '.wpl',
                  '.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg',
                  '.rm', '.swf', '.vob', '.wmv'],
    'compressed': ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.zip'],
    'disk_img': ['.bin', '.dmg', '.iso', '.toast', '.vcd'],
    'data_dbs': ['.csv', '.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml'],
    'email': ['.email', '.eml', '.emlx', '.msg', '.oft', '.ost', '.pst', '.vcf'],
    'executable': ['.apk', '.bat', '.bin', '.cgi', '.pl', '.com', '.exe', '.gadget', '.jar', '.msi', '.py', '.wsf'],
    'font': ['.fnt', '.fon', '.otf', '.ttf'],
    'image': ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff'],
    'internet': ['.asp', '.aspx', '.cer', '.cfm', '.cgi', '.pl', '.css', '.htm', '.html', '.js', '.jsp',
                 '.part', '.php', '.py', '.rss', '.xhtml'],
    'presentation': ['.key', '.odp', '.pps', '.ppt', '.pptx'],
    'text': ['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd', '.ods', '.xls', '.xlsm', '.xlsx'],
    'system': ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk', '.msi', '.sys', '.tmp']
}

form_names = {'folders': 'Folders', 'audio_vid': 'Media', 'compressed': 'Compressed', 'disk_img': 'Disk images', 'data_dbs': 'Data and Databases', 'email': 'Email related files',
              'executable': 'Programs', 'font': 'Fonts', 'image': 'Pictures', 'internet': 'Web related files', 'presentation': 'Slides', 'text': 'Text documents', 'system': 'Settings'}


test = [{'file': 'some file', 'topic_x': 'hello',
         'absolute_path': '../data/t5/000002.doc', 'extension': '.html'}]


@ app.route('/', methods=['POST'])
def open_file():
    filepath = request.form.get('filepath')
    os.popen(f"open {filepath}")

    return '', 204


@ app.route('/select-folders', methods=['POST'])
def index_folders():
    if request.method == 'POST':
        session['curr_folder'] = request.form.getlist('folder')

    return '', 204


@ app.route('/')
def index():
    home_folder = '/Users/faustina/METIS/BOOTCAMPWORK'
    if home_folder[-1] != '/':
        home_folder += '/'
    if ('curr_folder' not in session) or (not len(session['curr_folder'])):
        session['curr_folder'] = [home_folder]

    breadcrumbs = home_folder[1:].split('/')
    session['file_attrs'] = [get_attributes(file, home_folder) for file in os.listdir(
        home_folder) if os.path.isdir(home_folder + file)]

    no_files = len(session['file_attrs'])

    return render_template('index.html', current_folder=home_folder, breadcrumbs=breadcrumbs, nfiles=no_files, files=session['file_attrs'], icon=icon)


@ app.route('/home')
def homepage():
    folders = session['curr_folder']
    all_files = []

    for folder in folders:
        files = os.listdir(folder)
        all_files.extend([get_attributes(file, folder) for file in files])

    session['file_attrs'] = all_files

    return render_template('homepage.html', files=session['file_attrs'], icon=icon)


@app.route('/composition')
def composition():
    files_w_attributes = session['file_attrs']

    blind_cats = blind_categories(formats, files_w_attributes)
    blind_cats = {item: blind_cats[item] for item in sorted(
        blind_cats, key=lambda i: len(blind_cats[i]), reverse=True)}

    return render_template('composition.html', icon=icon, form_names=form_names, blind_categories=blind_cats)


@app.route('/indexer')
def indexer():

    return render_template('indexer.html')


if __name__ == '__main__':
    app.run(debug=True)
