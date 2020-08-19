#!/usr/bin/python3

import bs4 as bs4
import urllib.request as request
import os
import re
import sys
from tqdm import tqdm
from argparse import ArgumentParser

def argumnet_parser():

    """
    Parse command line arguments.
    Returns:  command line arguments
    """

    parser = ArgumentParser()
    parser.add_argument("-l", "--link", required=True, type=str,
                        help="Provide the link of the wallpaper collection not")
    return parser

def parse(web_url):

    """
    Parse the url and return the soup [HTML thingy]
    """
    if "://getwallpapers.com/" not in web_url:
        print("Please enter a valid getwallpapers.com url")
        sys.exit(1)

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
    args = argumnet_parser().parse_args()
    soup = parse(args.link)
    folder_name = folder_name(soup)
    download(soup, folder_name)
