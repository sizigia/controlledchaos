from tika import parser
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import chardet
import textract
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from collections import Counter, defaultdict
from flask import redirect, url_for


def get_attributes(filepath, folder):
    if not folder.endswith('/'):
        folder = folder + '/'

    file = folder + filepath
    file_stats = os.stat(file)
    attributes = {'parent_folder': folder,
                  'absolute_path': file,
                  'name': filepath,
                  'size_mb': file_stats.st_size / 1e+6,
                  'created_on': datetime.fromtimestamp(file_stats.st_birthtime),
                  'last_modified_on': datetime.fromtimestamp(file_stats.st_mtime)}

    if os.path.isdir(file):
        ext = 'folder'
    elif os.path.isfile(file):
        ext = filepath.split('.')[-1]
    else:
        ext = ''

    attributes['extension'] = ext

    return attributes


def blind_categories(format_dict, collection):
    blind_classifier = {k: list(collection.find(
        {"extension": {"$in": v}})) for k, v in format_dict.items()}

    for k, v in blind_classifier.items():
        [(file.pop('_id', None) and file.pop('text', None)) for file in v]

    blind_classifier = {item: blind_classifier[item] for item in sorted(
        blind_classifier, key=lambda i: len(blind_classifier[i]), reverse=True)}

    return blind_classifier


def extract_text(record, thresh=1000):
    text_ext = ['ppt', 'pptx', 'doc', 'docx', 'odt', 'pdf',
                'rtf', 'text', 'txt', 'wpd', 'ods', 'xls', 'xlsm', 'xlsx']

    if record['extension'] in text_ext:
        text = parser.from_file(record['absolute_path'], service='text')[
            'content'][:thresh]

    return text


def labels(corpus):
    params = {
        'vectorizer': {
            'analyzer': 'word',
            'stop_words': stopwords.words('english'),
            'ngram_range': (1, 1),
            'token_pattern': '[a-z]{3,}',
            'max_df': 0.1,
            'lowercase': True
        },
        'km_params': {
            'random_state': 30,
            'n_clusters': 10,
        }
    }

    tfidf = TfidfVectorizer(**params['vectorizer'])
    try:
        X = tfidf.fit_transform(corpus)
        km = KMeans(**params['km_params']).fit(X)
        return km.labels_
    except:
        return 404


def name_cluster_labels_common(sw, topic_files, words=8):
    cluster_names = {}

    for i in topic_files.keys():
        label_text = ' '.join([file['text'] for file in topic_files[i]])
        corpus = re.findall('[a-zA-Z]{4,}', label_text)
        corpus = [w for w in corpus if (w.lower() not in sw)]
        label_dict = Counter(corpus)
        cluster_names[i] = '-'.join([w[0]
                                     for w in label_dict.most_common(words)])

    return cluster_names


def get_topic_files(files):
    topic_files = defaultdict(list)

    for file in files:
        topic_files[file['topic']].append(file)

    topic_files = dict(topic_files)

    return topic_files
