from abc import ABC


class Loader(ABC):

    def load(self, save_path: str, phrase: str, count: int):
        """
        :param save_path: path for save images
        :param phrase: phrase for search
        :param count: download count
        """

# from data.loader_impl.bing_impl.bing_loader import BingLoader
from data.loader_impl.google_img.google_img_loader import GoogleLoader


def get_loader() -> Loader:
    """
    :return: Loader instance
    """
    return GoogleLoader()