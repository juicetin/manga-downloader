from abc import ABCMeta
from abc import abstractmethod

import requests
import shutil

class MangaDownloader:
    __metaclass__ = ABCMeta

    def __init__(self, url):
        self.base_url = url

    @abstractmethod
    def get_img_url_from_html(self, html):
        pass

    @abstractmethod
    def get_page_paths_from_html(self, html):
        pass

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
    
