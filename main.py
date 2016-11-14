from downloaders import mangareader_downloader, mangastream_downloader
import sys, getopt

# NOTE hacky solution for now. Amongst other things, introduce a checker for 
# which sources have requested chapters available and select an appropriate source 
# (or even mix things up)
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hm:c", ["manga=", "chapter="])
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
            chapter = arg

    print('Downloading chapter {} from manga: {}'.format(chapter, manga))

    mrd = mangareader_downloader.MangaReaderDownloader()
    msd = mangastream_downloader.MangaStreamDownloader()

    mrd.download_chapter(manga, chapter)
    msd.download_chapter(manga, chapter)

if __name__ == "__main__":
    main(sys.argv[1:])
