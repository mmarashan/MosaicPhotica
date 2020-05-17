import os
from urllib.parse import urljoin, urlparse

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

from data.loader import Loader, get_loader

# from prepare_data.razmetchik import run_prepare_set

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
theme_tag = "test"

load_path = "/home/maxim/Desktop/test"


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    """
    Returns all image URLs on a single `url`
    """
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        else:
            img_url = urljoin(url, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass
                # finally, if the url is valid
                if is_valid(img_url):
                    urls.append(img_url)
    print("Images urls {}".format(urls))
    return urls


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True,
                    unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main(url, path):
    # get all images
    imgs = get_all_images(url)
    for img in imgs:
        # for each image, download it
        download(img, path)


main("https://www.google.co.in/search?q=%D0%A2%D1%80%D0%BE%D0%B5%20%D1%80%D0%BE%D1%81%D1%81%D0%B8%D1%8F%D0%BD%20%D0%BF%D0%BE%D0%BF%D0%B0%D0%BB%D0%B8%20%D0%B2%20%D1%82%D0%BE%D0%BF-20%20%D0%B1%D0%BE%D0%B3%D0%B0%D1%82%D0%B5%D0%B9%D1%88%D0%B8%D1%85%20%D1%80%D0%B5%D0%B7%D0%B8%D0%B4%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%A1%D0%BE%D0%B5%D0%B4%D0%B8%D0%BD%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%9A%D0%BE%D1%80%D0%BE%D0%BB%D0%B5%D0%B2%D1%81%D1%82%D0%B2%D0%B0.%20%D0%A1%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%BD%D0%BE%20%D0%BD%D0%BE%D0%B2%D0%BE%D0%BC%D1%83%20%D1%80%D0%B5%D0%B9%D1%82%D0%B8%D0%BD%D0%B3%D1%83%2C%20%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D1%8B%D0%B9%20%D1%81%D0%BE%D1%81%D1%82%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0%20Sunday%20Times&tbm=isch",
     load_path)

# loader: Loader = get_loader()
# loader.load(load_path,
#             "Трое россиян попали в топ-20 богатейших резидентов Соединенного Королевства. Согласно новому рейтингу, который составила Sunday Times",
#             10)
# run_prepare_set(theme_tag, "С.П.Королев")
