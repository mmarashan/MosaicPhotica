import os
from mosaic.mosaic import create_mosaic

THIS_FILE_PATH = os.path.dirname(os.path.realpath(__file__))

img_path = "/home/maxim/Desktop/greenpeace.jpg"
source_dirs = ["/home/maxim/pho_mos/greenpeaceru"]
name_prefix = "greenpeace"

not_ukrup_fields=[(0.1, 0.0, 0.0, 0.9)]
cell_size=32

resize_factors_variants = [0.05, 0.06, 0.07]
ukrup_field_max_percent_variants = [0.06, 0.08, 0.1]


create_mosaic(
    img_path=img_path,
    source_dirs=source_dirs,
    name_prefix=name_prefix,
    resize_factors_variants=resize_factors_variants,
    cell_size=cell_size,
    ukrup_field_max_percent_variants=ukrup_field_max_percent_variants,
    not_ukrup_fields=not_ukrup_fields
)
