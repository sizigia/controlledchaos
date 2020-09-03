import pandas as pd
import chardet
import textract
from bs4 import BeautifulSoup

def process_file(row):
    filepath = row['absolute_path']
    ext = row['extension']
    
    return filepath, ext
    
    
def extract_raw_text(row, thresh=50000):
    filepath, ext = process_file(row)
    enc = chardet.detect(open(filepath, 'rb').readline())['encoding']
    text = ''
    
    try:
        if ext in ('.xls', '.pdf', '.doc'):
            text = textract.process(filepath, encoding=enc).decode()
        elif ext == '.html':
            text = BeautifulSoup(''.join(open(filepath, 'r', encoding=enc).readlines()).lower(), 'html.parser').get_text(separator=' ')
        elif ext == '.text':
            text = ' '.join(open(filepath, 'r', encoding=enc).readlines())
        else:
            pass
    except:
        pass
    
    if len(text) > thresh:
        text = text[:thresh]
        
    return text