import requests
from bs4 import BeautifulSoup
import sys
import os

url_stem = "https://thorns.thecomicseries.com/comics/"

root_dir = sys.argv[1]

start_num = 1

if not os.path.isdir(root_dir):
    print("Argument is not a directory")
    sys.exit()

def archive(comicNum):
    # element "comicimagelink" links to the next comic
    # if "comicimagelink" is null, we have reached the last comic page
    # element "comicimage" contains the image to be archived
    # return true if there is another page to be archived

    # scrape page and create a soup
    page_data = requests.get(url_stem + str(comicNum)).content
    soup = BeautifulSoup(page_data, "html.parser")

    # find and kill i mean download image
    image_url = str(soup.find(id="comicimage")).split("src=\"")[1].split("\"")[0]
    img_file = open(os.path.join(root_dir, str(comicNum) + ".png"), "xb")
    img_file.write(requests.get(image_url).content)
    img_file.close()
    print("Archived page " + str(comicNum))

    # if you can't click to go to the next comic, stop progressing
    if str(soup.find(id="comicimagelink")) != "None":
        return True
    return False


keepArchiving = True

while keepArchiving:
    keepArchiving = archive(start_num)
    start_num += 1