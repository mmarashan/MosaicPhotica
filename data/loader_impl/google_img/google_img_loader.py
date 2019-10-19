from bs4 import BeautifulSoup
import traceback
import os
import urllib.request as url_req
import json

from util.logs import get_logger

LOGGER = get_logger("GOOGLE_IMG_LOADER")

from urllib.parse import quote
from data.loader import Loader


class GoogleLoader(Loader):

    def load(self, save_path: str, phrase: str, count: int):
        """
        :param save_path: name of theme
        :param phrase: phrase for search
        :param count: name of theme
        :return: path to folder with result
        """

        image_prefix = phrase
        query = quote(phrase).split()
        query = '+'.join(query)
        url = "https://www.google.co.in/search?q=" + query + "&tbm=isch"
        LOGGER.debug("Download from " + url)
        # add the directory for your image here

        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
            }
        soup: BeautifulSoup = BeautifulSoup(url_req.urlopen(url_req.Request(url, headers=header)),
                                            'html.parser',
                                            from_encoding='ISO-8859-5')

        images_list = []  # contains the link for Large original images, type of  image
        for a in soup.find_all("div", {"class": "rg_meta"}, limit=count):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            images_list.append((link, Type))

        LOGGER.debug("There are total" + str(len(images_list)) + "images")

        # create dir
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        THEME_RESULT_DIR = save_path

        if not os.path.exists(THEME_RESULT_DIR):
            os.mkdir(THEME_RESULT_DIR)

        counter = 0

        # download images
        for i, (img_link, Type) in enumerate(images_list):

            try:
                LOGGER.debug("Try download " + img_link)
                request_result = url_req.urlopen(img_link)
                raw_img = request_result.read()

                count_img_in_dir = len([i for i in os.listdir(THEME_RESULT_DIR) if image_prefix in i]) + 1

                if len(Type) == 0:
                    f = open(os.path.join(THEME_RESULT_DIR, image_prefix + "_" + str(count_img_in_dir) + ".jpg"), 'wb')
                else:
                    f = open(os.path.join(THEME_RESULT_DIR, image_prefix + "_" + str(count_img_in_dir) + "." + Type),
                             'wb')

                f.write(raw_img)
                f.close()

                LOGGER.debug("Success download")

                counter = counter + 1
                if counter == count:
                    LOGGER.debug("Counter " + str(count_img_in_dir) + " success download image")
                    break

            except Exception:
                LOGGER.error("Could not load : " + str(img_link))
                LOGGER.error(str(traceback.format_exc()))

        if len(images_list) < count:
            LOGGER.warning("Warning! Less than " + str(count) + " images was downloaded!")
