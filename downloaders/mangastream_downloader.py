import requests
from urllib import request
from pyquery import PyQuery as pq
import pdb
import os, sys

import ctypes

from downloaders import download_base

def glibc_fix():
    libc = ctypes.cdll.LoadLibrary('libc.so.6')
    res_init = libc.__res_init
    res_init()

class MangaStreamDownloader(download_base.MangaDownloader):
    def __init__(self):
        super().__init__(url='http://www.mangastream.com')

    def get_img_url_from_html(self, url):
        """
        Extracts image url from page containing image
        """
        html = self.get_page_html_decode_utf8(first_url)
        q = pq(html)
        img_url = q("#manga-page").attr('src')
        return img_url
    
    def get_page_paths_from_html(self, html):
        """
        Extracts list of page paths from any given page of the chapter. Assumes
        that every page of chapters will contain the dropdown menu to select page
        """
        q = pq(html)
        dropdown_options = q('.btn-reader-page').children('ul').children('li')
        page_paths = [pq(d).children('a').attr('href') for d in dropdown_options]
        return page_paths
    
    def get_chapter_url(self, manga, chapter):
        url = 'http://mangastream.com/manga/{}'.format(manga)
        html = self.get_page_html_decode_utf8(url)
        q = pq(html)
        chapter_table_items = q('.table-striped').find('a')
        chapter_urls = [pq(item).attr('href') for item in chapter_table_items if str(chapter) in pq(item).attr('href')]
        try:
            return chapter_urls[0]
        except IndexError:
            self.cleanup(manga, chapter)
            return -1

    def format_manga_name(self, name):
        name_parts = name.lower().split(' ')
        return '_'.join(name_parts)

    def get_downloader_name(self):
        return str(self.__class__()).split('.')[2].split(' ')[0]
    
    def download_chapter_succcessfully(self, manga, chapter):
        """
        Downloads specific chapter of manga
        """

        # Get URL
        glibc_fix()
        manga_fmtd = self.format_manga_name(manga)
        first_url = self.get_chapter_url(manga_fmtd, chapter)

        if first_url == -1:
            print('Chapter: {} for manga: {} not found on MangaStream.'.format(chapter, manga))
            self.cleanup(manga, chapter)
            return False
        else:
            # Get list of chapter page URLs
            html = self.get_page_html_decode_utf8(first_url)
            page_paths = self.get_page_paths_from_html(html)

            # Prepare directory
            chapter_str = str(chapter)
            os.makedirs('{}'.format(chapter_str))

            # Download every page
            for num, page_path in enumerate(page_paths):
                page_url = page_path
                self.download_img_from_url(page_url, '{}/{}.jpg'.format(chapter_str, self.pad_number(num)))

            return True
