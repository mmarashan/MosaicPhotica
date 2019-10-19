import os
from mosaic.mosaic import create_mosaic

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))


# create_mosaic(
#     img_path="/home/maxim/Desktop/vkhack.jpg",
#     source_dirs=["/home/maxim/Desktop/my_photo_sample", "/home/maxim/Desktop/mosaic_element"],
#     target_path=THIS_FILE_PATH + "/test/me2.jpg",
#     resize_factor=0.27,
#     cell_size=32,
#     ukrup_field_max_percent=0.1,
#     not_ukrup_fields=[(0.3, 0.2, 0.70, 0.65)]
# )
#

create_mosaic(
    img_path="/home/maxim/Desktop/леонов.jpg",
    source_dirs=["/home/maxim/Desktop/leonov"],
    target_path=THIS_FILE_PATH + "/test/leonov.jpg",
    resize_factor=0.17,
    cell_size=32,
    ukrup_field_max_percent=0.1,
    not_ukrup_fields=[(0.15, 0.08, 0.60, 0.65)]
)
