import os
import re
import pickle
from datetime import datetime
from helpers import get_attributes, blind_categories

import pandas as pd
from flask import Flask, flash, render_template, request, url_for, redirect, session

app = Flask(__name__)


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

form_names = {'audio_vid': 'Media', 'compressed': 'Compressed', 'disk_img': 'Disk images', 'data_dbs': 'Data and Databases', 'email': 'Email related files',
              'executable': 'Programs', 'font': 'Fonts', 'image': 'Pictures', 'internet': 'Web related files', 'presentation': 'Slides', 'text': 'Text documents', 'system': 'Settings'}


test = [{'file': 'some file', 'topic_x': 'hello',
         'absolute_path': '../data/t5/000002.doc', 'extension': '.html'}]


@ app.route('/', methods=['POST'])
def open_file():
    filepath = request.form.get('filepath')
    os.popen(f"open {filepath}")

    return '', 204


@ app.route('/', methods=['POST'])
def index_folders():
    print(request.form.getlist('folder'))
    folders = request.form.getlist('folder')

    return redirect(url_for('homepage', folders=folders))


@ app.route('/')
def index():
    home_folder = '/Users/faustina/'
    breadcrumbs = home_folder[1:].split('/')
    files = [get_attributes(file, home_folder)
             for file in os.listdir(home_folder) if os.path.isdir(home_folder + file)]
    no_files = len(files)

    return render_template('index.html', current_folder=home_folder, breadcrumbs=breadcrumbs, nfiles=no_files, files=files, icon=icon)


@ app.route('/home')
def homepage(folders=['/Users/faustina/']):
    # METIS/BOOTCAMPWORK/Project5/controlledchaos/data/t5/
    all_files = []

    for folder in folders:
        breadcrumbs = folder[1:].split('/')
        all_files.extend([get_attributes(file, folder)
                          for file in os.listdir(folder) if file != '.DS_Store'])

    return render_template('homepage.html', breadcrumbs=breadcrumbs, files=all_files, icon=icon)


@app.route('/composition')
def composition():
    # METIS/BOOTCAMPWORK/Project5/controlledchaos/data/t5/'
    current_folder = '/Users/faustina/METIS/BOOTCAMPWORK/Project5/controlledchaos/data/t5/'
    breadcrumbs = current_folder[1:].split('/')
    blind_cats = blind_categories(formats, os.listdir(current_folder))
    blind_cats = {item: [get_attributes(file, current_folder) for file in blind_cats[item]]
                  for item in sorted(blind_cats, key=lambda i: len(blind_cats[i]), reverse=True)}

    return render_template('composition.html', breadcrumbs=breadcrumbs, icon=icon, form_names=form_names, blind_categories=blind_cats)


@app.route('/indexer')
def indexer():

    return render_template('indexer.html')

# @ app.route('/browser')
# def index2():
#    user_agent = request.headers.get('User-Agent')
#    return '<p>Your browser is %s</p>' % user_agent


if __name__ == '__main__':
    app.run(debug=True)
