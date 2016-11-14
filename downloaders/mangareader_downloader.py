import requests
from urllib import request
from pyquery import PyQuery as pq
import pdb
import os

from downloaders import download_base

class MangaReaderDownloader(download_base.MangaDownloader):
    def __init__(self):
        super().__init__(url='http://www.mangareader.net')

    def get_img_url_from_html(self, html):
        """
        Extracts image url from page containing image
        """
        q = pq(html)
        img_url = q("#img").attr('src')
        return img_url
    
    def get_page_paths_from_html(self, html):
        """
        Extracts list of page paths from any given page of the chapter. Assumes
        that every page of chapters will contain the dropdown menu to select page
        """
        q = pq(html)
        dropdown_options = q("#pageMenu").children('option')
        page_paths = [pq(d).attr('value') for d in dropdown_options]
        return page_paths

    def format_manga_name(self, name):
        name_parts = name.lower().split(' ')
        return '-'.join(name_parts)

    def download_chapter(self, manga, chapter):
        """
        Downloads specific chapter of manga
        """
        manga = self.format_manga_name(manga)
        first_url = '{}/{}/{}'.format(self.base_url, manga, chapter)
        html = request.urlopen(first_url).read().decode('utf-8')

        page_paths = self.get_page_paths_from_html(html)
        if len(page_paths) == 0:
            print('Chapter: {} for manga: {} not found on MangaReader.'.format(chapter, manga))
            self.cleanup(manga, chapter)

        else:
            chapter_str = str(chapter)
            os.makedirs('{}'.format(chapter_str))
            for num, page_path in enumerate(page_paths):
                page_url = '{}{}'.format(self.base_url, page_path)
                self.download_img_from_url(page_url, '{}/{}.jpg'.format(chapter_str, self.pad_number(num)))
