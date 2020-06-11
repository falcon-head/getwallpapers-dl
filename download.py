#!/usr/bin/python3

import bs4 as bs4
import urllib.request as request
import os
import re
import sys
from tqdm import tqdm

def verify_arg():

    """
    Check for the arguments, and check if it is correct or not

    Returns:
        url [String] : Returns a page url to donwload the wallpapers
    """

    if len(sys.argv) == 1:
        print("Please provide the link of the wallpaper collection link")
        sys.exit(1)
    elif len(sys.argv) == 2:
        try:
            if "://getwallpapers.com/" in str(sys.argv[1]):
                url = str(sys.argv[1])
        except ValueError as e:
            print("Please enter a valid url")
            sys.exit(1)
    else:
        print("Too many arguments")
        sys.exit(1)

    return url

def parse(web_url):

    """
    Parse the url and return the soup [HTML thingy]
    """

    url = request.urlopen(web_url)
    soup = bs4.BeautifulSoup(url, 'lxml')
    return soup

def folder_name(soup):


    """
    Get the title from the html and create a directory out of it
    """

    title = soup.title.string
    directory = title
    path = os.path.dirname(os.path.realpath(__file__))
    final_directory = os.path.join(path, directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    return final_directory

def download(soup, folder_name):

    """
    Parse the soup to get the url of the image. Combine it with the main url and pass the path of the folder to store
    and download all the images.
    """

    for url in tqdm(soup.findAll('a', attrs={"class": "download_button"})):
        downloadable_url = url.get('href')
        final_url = request.urljoin('http://getwallpapers.com', downloadable_url)
        get_name = re.compile(r'(?:.(?!/))+$')
        file_name = get_name.search(downloadable_url)
        file_name = file_name.group(0).rsplit('/')[1]
        fullfilename = os.path.join(folder_name, file_name)
        request.urlretrieve(final_url, fullfilename)

if __name__ == "__main__":
    url = verify_arg()
    soup = parse(url)
    folder_name = folder_name(soup)
    download(soup, folder_name)
