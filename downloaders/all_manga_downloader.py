from downloaders import mangareader_downloader, mangastream_downloader

class AllSourceMangaDownloader():
    def __init__(self):
        mrd = mangareader_downloader.MangaReaderDownloader()
        msd = mangastream_downloader.MangaStreamDownloader()
        self.downloaders = [mrd, msd]

    def download_chapter(self, manga, chapter):
        for downloader in self.downloaders:
            if (downloader.download_chapter_succcessfully(manga, chapter) == True):
                break
