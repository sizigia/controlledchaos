import os
import pickle
import re
from collections import Counter, defaultdict
from datetime import datetime

import chardet
import pandas as pd
import pymongo
import textract
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from tika import parser

from helpers import (blind_categories, extract_text, get_attributes,
                     get_topic_files, labels, name_cluster_labels_common)

project_folder = os.path.expanduser(
    '~/METIS/BOOTCAMPWORK/Project5/controlledchaos/app/')  # the folder of your project
load_dotenv(os.path.join(project_folder, '.env'))

MONGODBNAME = os.getenv("MONGODBNAME")

client = pymongo.MongoClient()
db = client[MONGODBNAME]
curr_files_db = db['curr_files']

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mockupkey'
app.config['SESSION_TYPE'] = 'filesystem'


icon = {
    'folder': 'folder',
    'jpg': "file-image",
    'pdf': "file-earmark-richtext",
    'html': "file-post",
    'ppt': 'file-slides',
    'xls': 'file-spreadsheet',
    'text': "file-earmark-text",
    'txt': "file-earmark-text",
    'doc': 'file-earmark-font',
    'no-icon': "file-x"
}

formats = pickle.load(open('data/formats.pkl', 'rb'))
form_names = {'folder': 'Folders', 'audio_vid': 'Media', 'compressed': 'Compressed', 'disk_img': 'Disk images', 'data_dbs': 'Data and Databases', 'email': 'Email related files',
              'executable': 'Programs', 'font': 'Fonts', 'image': 'Pictures', 'internet': 'Web related files', 'presentation': 'Slides', 'text': 'Text documents', 'system': 'Settings'}

custom_sw = pickle.load(open('data/stopwords.pkl', 'rb'))


@ app.route('/', methods=['POST'])
def open_file():
    filepath = request.form.get('filepath')
    os.popen('open "{}"'.format(filepath))

    return '', 204


@ app.route('/select-folders', methods=['POST'])
def index_folders():
    if request.method == 'POST':
        folders = request.form.getlist('folder')
        if not len(folders):
            folders = session['curr_folder']

    if (folders != session['curr_folder']):
        curr_files_db.delete_many({})

        all_files = []

        for folder in folders:
            files = os.listdir(folder)[:200]
            curr_files_db.insert_many(
                [get_attributes(file, folder) for file in files])

        session['curr_folder'] = folders

    return '', 204


@ app.route('/')
def index():
    # hardcoded
    #home_folder = '/Users/faustina/METIS/BOOTCAMPWORK/Project5/controlledchaos/data/'
    home_folder = '/Users/faustina/Documents/'

    if home_folder[-1] != '/':
        home_folder += '/'

    session['curr_folder'] = [home_folder]

    breadcrumbs = home_folder[1:].split('/')
    folders_attrs = [get_attributes(file, home_folder) for file in os.listdir(
        home_folder) if os.path.isdir(home_folder + file)]

    nfolders = len(folders_attrs)
    session['folder_attrs'] = folders_attrs

    # flash when there are no folders

    return render_template('index.html', current_folder=home_folder, breadcrumbs=breadcrumbs, nfolds=nfolders, files=folders_attrs, icon=icon)


@ app.route('/home')
def homepage():
    cursor = curr_files_db.find({})
    entries = list(cursor)

    return render_template('homepage.html', files=entries, icon=icon, format_names=form_names)


@app.route('/composition')
def composition():
    # print(request.url_rule.rule)
    blind_cats = blind_categories(formats, curr_files_db)

    return render_template('composition.html', icon=icon, form_names=form_names, blind_categories=blind_cats)


@app.route('/indexer')
def indexer():
    topic_files = pickle.load(open('data/This_Directory_is_a_Mess.pkl', 'rb'))

    return render_template('indexer.html', topic_files=topic_files, icon=icon)


if __name__ == '__main__':
    app.run(debug=True)
