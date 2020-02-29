import os
from app.data_base import video
import jieba
from wordcloud import WordCloud
import cv2
import numpy
from PIL import Image

from time import time


def jieba_cut(text):
    cut = jieba.cut(text)
    words = ' '.join(cut)
    return words


def word_cloud(words):
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    font_path = root_path + '/Hiragino Sans GB W3.otf'
    wc = WordCloud(font_path=font_path,
                   background_color='white',
                   width=1000,
                   height=800
                   ).generate(words)
    return wc


def ciyun(av):
    t1 = time()
    # result = video.read(av)
    result = video.replies(av)
    t2 = time()
    print('拿到原始数据花了', t2-t1)
    text = ''
    # for item in result['danmus']:
    #     text += item['content']
    # for item in result['replies']:
    #     text += item['content']
    for item in result:
        text += item['content']
    t3 = time()
    print('数据拼接花了', t3-t2)
    wc = word_cloud(jieba_cut(text))
    a = wc.to_array()
    t4 = time()
    print('分词+wc用了', t4-t3)
    buf = cv2.imencode('.png', a)[1]
    bytes_image = Image.fromarray(numpy.uint8(buf)).tobytes()
    t5 = time()
    print('转成图片流用了', t5-t4)
    return bytes_image
