from downloaders import all_manga_downloader
import sys, getopt
import numpy as np
import pdb
from multiprocessing import Pool

# NOTE hacky solution for now. Amongst other things, introduce a checker for 
# which sources have requested chapters available and select an appropriate source 
# (or even mix things up)

def download_chapter(manga, chapter):
    print('Downloading chapter {} from manga: {}'.format(chapter, manga))

    all_source_manga_downloader = all_manga_downloader.AllSourceMangaDownloader()
    all_source_manga_downloader.download_chapter(manga, chapter)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hm:c", ["manga=", "chapter=", "chapters="])
        argv[0]
    except getopt.GetoptError:
        print('main.py -m <manga> -c <chapter>')
        sys.exit(2)
    except IndexError:
        print('main.py -m <manga> -c <chapter>')
        sys.exit(2)
  
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -m <manga> -c <chapter>')
            sys.exit()
        elif opt in ("-m", "--manga"):
            manga = arg
        elif opt in ("-c", "--chapter"):
            chapters = [arg]
        elif opt in ("-chs", "--chapters"):
            parts = arg.split('-')
            start = int(parts[0])
            end = int(parts[1])
            chapters = list(range(start, end+1))

    p = Pool(4)
    p.starmap(download_chapter, zip(np.repeat(manga, len(chapters)), chapters))

if __name__ == "__main__":
    main(sys.argv[1:])
