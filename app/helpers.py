import os
import re
from datetime import datetime


def get_attributes(filepath, folder):
    file = folder + filepath
    file_stats = os.stat(file)
    attributes = {'parent_folder': folder,
                  'name': filepath,
                  'size_mb': file_stats.st_size / 1e+6,
                  'created_on': datetime.fromtimestamp(file_stats.st_birthtime),
                  'last_modified_on': datetime.fromtimestamp(file_stats.st_mtime)}

    if os.path.isdir(file):
        ext = 'folder'
        attributes['nfiles'] = len(os.listdir(file))
    elif os.path.isfile(file):
        ext = '.' + filepath.split('.')[-1]
    else:
        ext = ''

    attributes['extension'] = ext

    return attributes


def blind_categories(format_dict, files):
    blind_classifier = {}

    for k, v in format_dict.items():
        blind_classifier[k] = [
            e for e in files if (f".{e.split('.')[-1]}" in v)]

    return blind_classifier
