#!/bin/env python
import zipfile, os, argparse
try: 
    import music_tag
except ImportError:
    print("Please install the 'music-tag' python package. Check the README for more details.")
    exit()

parser = argparse.ArgumentParser(description='Unzip zipfiles downloaded from Bandcamp.com into directories labelled by album.', epilog="https://github.com/qweri0p/myPyScripts")
parser.add_argument('-v', '--verbose', help="Display individual items being extracted.", action='store_true', default=False)
parser.add_argument('-q', '--quiet', help="Do not display any information at all.", action='store_true', default=False)
parser.add_argument('-c', '--clean', help="Removes zipfile once completed", action='store_true', default=False)
parser.add_argument('-d', '--dir', help="Runs the program in the specified directory.", default=".")
parser.add_argument('zips', metavar="zipfiles", help="Only unzips specified zipfiles.", nargs='*')
args = parser.parse_args()

files = os.listdir(args.dir)
albums = []

if args.zips:
    for i in args.zips:
        albums.append(i.split(".zip")[0])
else:
    for i in files:
        if i.endswith(".zip"):
            albums.append(i.split(".zip")[0])

for i in albums:
    with zipfile.ZipFile(args.dir + "/" + i + ".zip", "r") as zip_ref:
        os.mkdir(args.dir + "/" + 'temp')
        templist = zip_ref.namelist()
        if args.quiet == False:
            print("Starting: " + i)
        for j in templist:
            if args.verbose ==True:
                print("Extracting " + j)
            zip_ref.extract(j, args.dir + "/" + 'temp')
            if j.endswith(".mp3") or j.endswith(".wav") or j.endswith(".flac") or j.endswith(".ogg") or j.endswith(".aac") or j.endswith(".alac") or j.endswith(".aiff"):
                musicFile = music_tag.load_file(os.path.join(".", args.dir + "/" + 'temp',j))
                album = str(musicFile['album'])
                artist = str(musicFile['artist'])
                os.rename(os.path.join(args.dir + "/" + 'temp',j),os.path.join(args.dir + "/" + 'temp',j[len(artist)+len(album)+6:]))
        if args.quiet == False:
            print("Finished: " +artist + " - " + album)
        if args.clean == True:
            os.remove(args.dir + "/" + i + ".zip")
        os.rename(args.dir + "/" + 'temp', args.dir + "/" + album)
