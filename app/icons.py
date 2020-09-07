import pickle

icons = {
    'folder': 'folder',
    '.jpg': "file-image",
    '.pdf': "file-earmark-richtext",
    '.ppt': '',
    '.xls': '',
    '.text': "file-earmark-text",
    'no-icon': "file-x"
}


def update_icons():
    return pickle.dump(icons, open('icon.pkl', 'wb'))
