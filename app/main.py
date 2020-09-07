from flask import Flask, request, render_template, render_template_string
import pickle
from icons import update_icons
import os
app = Flask(__name__)

# update_icons()

#icon = pickle.load(open('icon.pkl', 'rb'))

icon = {
    'folder': 'folder',
    '.jpg': "file-image",
    '.pdf': "file-earmark-richtext",
    '.ppt': '',
    '.xls': '',
    '.text': "file-earmark-text",
    'no-icon': "file-x"
}


test = [{'file': 'Folder A', 'topic_x': 'hello',
         'absolute_path': '#', 'extension': 'folder'},
        {'file': 'filename1', 'topic_x': 'hello',
         'absolute_path': '#', 'extension': '.pdf'},
        {'file': 'filename2', 'topic_x': 'hello',
         'absolute_path': '#', 'extension': '.jpg'},
        {'file': 'filename2', 'topic_x': 'hello',
         'absolute_path': '#', 'extension': '.xls'},
        {'file': 'image something', 'topic_x': 'hello',
         'absolute_path': '#', 'extension': '.jpg'},
        {'file': 'image something', 'topic_x': 'hello',
         'absolute_path': '#', 'extension': '.text'}]


@ app.route('/<name>')
def index(name, rows=test):
    name = name.capitalize()
    os.chdir('')

    return render_template('index.html', name=name, rows_len=len(test), rows=test, icon=icon)


@ app.route('/')
def index2():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent


if __name__ == '__main__':
    app.run(debug=True)
