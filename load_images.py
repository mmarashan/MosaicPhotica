import os
from data.loader import Loader, get_loader
# from prepare_data.razmetchik import run_prepare_set

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
theme_tag = "love"

load_path = "/home/maxim/Desktop/leonov" #THIS_FILE_PATH+"/"+theme_tag

loader: Loader = get_loader()
# loader.load(load_path, "центр подготовки космонавтов", 35)
#loader.load(load_path, "тренировка космонавтов", 35)
loader.load(load_path, "молодой алексей леонов", 30)
# run_prepare_set(theme_tag, "С.П.Королев")

import instaloader
