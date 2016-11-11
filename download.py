import requests
from urllib import request
from pyquery import PyQuery as pq
import shutil
import pdb
import os

def get_img_url_from_html(html):
    q = pq(html)
    img_url = q("#img").attr('src')
    return img_url

def get_page_count_from_html(html):
    q = pq(html)
    dropdown_options = q("#pageMenu").children('option')
    page_paths = [pq(d).attr('value') for d in dropdown_options]
    return page_paths

def download_img_from_url(page_url, filename):
    img_url = get_img_url_from_html(page_url)
    print('Downloading image from url: {}'.format(img_url))
    # opener.retrieve(img_url, filename)
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def download_chapter(manga, chapter):
    base = 'http://www.mangareader.net'
    first_url = '{}/{}/{}'.format(base, manga, chapter)
    html = request.urlopen(first_url).read().decode('utf-8')
    page_paths = get_page_count_from_html(html)
    chapter_str = str(chapter)
    os.makedirs('{}'.format(chapter_str))
    for num, page_path in enumerate(page_paths):
        page_url = '{}{}'.format(base, page_path)
        download_img_from_url(page_url, '{}/{}.jpg'.format(chapter_str, num))
