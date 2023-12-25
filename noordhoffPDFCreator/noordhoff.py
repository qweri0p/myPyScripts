#!/bin/env python
import requests, img2pdf, argparse, os, re

parser = argparse.ArgumentParser(description='Download books from Noordhoff.', epilog="https://gist.github.com/qweri0p/04519b28504af179287edc6970935cc7")
parser.add_argument('-v', '--verbose', help="display individual images downloaded", action='store_true', default=False)
parser.add_argument('-o', '--output', help="rename the pdf to specified name.", default="output", action='store')
parser.add_argument('link', metavar="link", help="link to the image source.", nargs=1)
args = parser.parse_args()

def main():
    dirname = "temp"
    # example link: https://cdp.contentdelivery.nu/f5c5e97e-5f64-4da4-a3dd-d99154e8338d/20221004094415/extract/assets/img/layout/1.jpg
    # I need to extract: f5c5e97e-5f64-4da4-a3dd-d99154e8338d/20221004094415
    # REGEX TIME!!! YAAAAAY!!
    # [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\/[0-9]+
    # That should work fine
    bookID = re.search("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\/[0-9]+", args.link[0])
    #it works :)
    if args.verbose:
        print("Selected book Identifier: "+bookID.group()+".")
    os.mkdir(dirname)
    if args.verbose:
        print("Created '"+dirname+"' directory.")

    fulllink = "https://cdp.contentdelivery.nu/"+bookID.group()+"/extract/assets/img/layout/"
    print("Downloading images from "+fulllink+".")
    running = True
    index = 1
    while running:
        r = requests.get(fulllink + str(index) + ".jpg")
        if r.status_code == 200:
            if args.verbose:
                print("Downloading "+r.url+".")
            with open(dirname+"/"+str(index)+".jpg", 'wb') as f:
                f.write(r.content)
        else:
            running = False
        index+=1
    print("Downloaded every page.")
    print("Creating PDF.")
    imgs = []
    imgpaths = []
    for fname in os.listdir(dirname):
        if not fname.endswith(".jpg"):
            continue
        path = os.path.join(dirname, fname)
        if os.path.isdir(path):
            continue
        imgs.append(fname)
    imgs = sorted([int(x[:-4]) for x in imgs]) 
    imgpaths = [dirname+"/"+str(x)+".jpg" for x in imgs]
    with open(args.output+".pdf","wb") as f:
        f.write(img2pdf.convert(imgpaths))
    print("Done.")

    listofdumbfiles = os.listdir(dirname)
    for dumbfile in listofdumbfiles:
        os.remove(os.path.join(dirname, dumbfile))
    os.rmdir(dirname)

if __name__ == "__main__":
    main()