import os
from data.loader import Loader, get_loader
# from prepare_data.razmetchik import run_prepare_set

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
theme_tag = "2020"

load_path = "/home/maxim/Desktop/2020"

loader: Loader = get_loader()
loader.load(load_path, "new year moskow", 50)
# loader.load(load_path, "christmas", 50)
loader.load(load_path, "new year salut", 50)
# run_prepare_set(theme_tag, "С.П.Королев")

import instaloader
