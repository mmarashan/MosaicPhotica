from azure.cognitiveservices.search.imagesearch.models import Images, ImageType, ImageSize
import traceback
import os
import urllib.request as url_req
import json

from util.logs import get_logger
from util.parallel import parallel_download

LOGGER = get_logger("BING_IMG_LOADER")

from data.loader import Loader

subscription_key = "c6cfe1a1d42b452398ed52d65382ea9f"
search_url = "https://api.cognitive.microsoft.com/bing/v5.0/images"

from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

class BingLoader(Loader):


    def load(self, save_path: str, phrase: str, count: int) -> str:
        """
        :param save_path: name of theme
        :param phrase: phrase for search
        :param count: name of theme
        :return: path to folder with result
        """
        image_prefix = phrase
        client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key),
                                base_url='https://api.cognitive.microsoft.com/bing/v5.0')
        image_results: Images = client.images.search(query=phrase,
                                                     size = ImageSize.small)
        print("Search result: " + str(image_results) + str(type(image_results)))
        result_dict = image_results.as_dict()
        images_list = [(a['content_url'], a['encoding_format']) for a in result_dict['value']]
        print("images: " + str(images_list))

        # create dir
        if not os.path.exists(save_path):
                    os.mkdir(save_path)
        THEME_RESULT_DIR = save_path

        if not os.path.exists(THEME_RESULT_DIR):
                    os.mkdir(THEME_RESULT_DIR)


        clear_urls = []

        # download images
        for i, (img_link, format) in enumerate(images_list):
            if len(format) == 0 or str(format) in ['gif', 'animatedgif']:
                continue
            clear_urls.append(img_link)

        result = parallel_download(clear_urls, THEME_RESULT_DIR, count, image_prefix)
        if result:
            LOGGER.debug("Success download image")

        return THEME_RESULT_DIR
