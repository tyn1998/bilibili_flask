import os
import shutil
from app.data_access.DB import DB
from app.data_access import bilibilier


def init_directory():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    images_path = root_path + '/word_cloud_images/'
    if os.path.exists(images_path):
        shutil.rmtree(images_path)
    os.mkdir(root_path + '/word_cloud_images/')


def init():
    init_directory()
    DB.reset()


def build_all(uid):
    bilibilier.build_all_continue(uid)


# build_all('2')

from app.data_access import video
x = video.read_comprehensive('0')
print(x)