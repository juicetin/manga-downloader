from abc import ABCMeta
from abc import abstractmethod
import os, sys

import requests
import shutil

class MangaDownloader:
    __metaclass__ = ABCMeta

    def __init__(self, url):
        self.base_url = url

    @abstractmethod
    def download_chapter_succcessfully(self, manga, chapter):
        pass

    @abstractmethod
    def get_img_url_from_html(self, html):
        pass

    @abstractmethod
    def get_page_paths_from_html(self, html):
        pass

    @abstractmethod
    def format_manga_name(self, name):
        pass

    # This is currently here if in future we want to 
    #   download chapters from a specific source exclusively
    def download_chapter(self, manga, chapter):
        return self.download_chapter_succcessfully(manga, chapter)

    def pad_number(self, num):
        """
        Pads a number with zeroes so it is 3 digits long
        """
        num_str = str(num)
        return '0' * (3-len(num_str)) + num_str

    def download_img_from_url(self, page_url, filename):
        """
        Given the page containing the image, extract the image url and save it
        to the specified file
        """
        img_url = self.get_img_url_from_html(page_url)
        print('Downloading image from url: {} as {}'.format(img_url, filename))
        # opener.retrieve(img_url, filename)
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    
    def download_chapters(self, manga, chapter_nums):
        """
        Downloads a list of chapters for a given manga
        """
        for chapter_num in chapter_nums:
            self.download_chapter(manga, chapter_num)

    def cleanup(self, manga, chapter):
        try:
            os.rmdir('{}'.format(chapter))
        except FileNotFoundError:
            pass
        print()
