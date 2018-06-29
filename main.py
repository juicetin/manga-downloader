from downloaders import all_manga_downloader
import sys, getopt
import numpy as np
import pdb
import argparse
from multiprocessing import Pool

# NOTE hacky solution for now. Amongst other things, introduce a checker for 
# which sources have requested chapters available and select an appropriate source 
# (or even mix things up)

def download_chapter(manga, chapter):
    print('Downloading chapter {} from manga: {}'.format(chapter, manga))

    all_source_manga_downloader = all_manga_downloader.AllSourceMangaDownloader()
    all_source_manga_downloader.download_chapter(manga, chapter)

def download_chapters_in_parallel_for_manga(manga, chapters):
    p = Pool(8)
    manga_chapter_tuples = zip(np.repeat(manga, len(chapters)), chapters)
    p.starmap(download_chapter, manga_chapter_tuples) 

def get_chapters_from_range(string):
    parts = string.split('-')
    start = int(parts[0])
    end = int(parts[1])
    chapters = list(range(start, end+1))
    return chapters

def main(argv):
    parser = argparse.ArgumentParser(description='downloads manga as a cli tool')
    parser.add_argument('--manga', type=str, help='name of the manga to dowlnoad')
    parser.add_argument('--chapter', type=int, help='chapter number to be downloaded')
    parser.add_argument('--chapters', type=str, help='chapter range to be downloaded - hyphen delimeted inclusive start and end, e.g. 1-176')

    args = parser.parse_args()

    manga = args.manga
    chapters = get_chapters_from_range(args.chapters)

    download_chapters_in_parallel_for_manga(manga, chapters)

if __name__ == "__main__":
    main(sys.argv[1:])
