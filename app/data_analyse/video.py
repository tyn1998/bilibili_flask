import time
import os
import jieba
from wordcloud import WordCloud

N = 100


def str2sec(x):
    m, s = x.strip().split(':') #.split()函数将其通过':'分隔开，.strip()函数用来除去空格
    return int(m)*60 + int(s)


def str2stamp(str):
    time_array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    stamp = int(time.mktime(time_array))
    return stamp


def income(view_count):
    income = int(view_count * 0.003)
    return income


def danmu_v_time_distribution(danmus, length):
    length = str2sec(length)
    distribution = [0]*N
    for item in danmus:
        index = int(float(item['time'])/length * N)
        if index >= N:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', index)
            index = N-1
        distribution[index] += 1
    distribution = ','.join(str(i) for i in distribution)
    return distribution


def danmu_bj_time_distribution(danmus, created):
    created = str2stamp(created)
    stamp_array = []
    for item in danmus:
        stamp_array.append(str2stamp(item['beijing_time']))
    latest = max(stamp_array)
    distribution = [0]*N
    for item in stamp_array:
        index = int((item-created)/(latest+0.01-created) * N)
        distribution[index] += 1
    distribution = ','.join(str(i) for i in distribution)
    return distribution


def reply_bj_time_distribution(replies, created):
    created = str2stamp(created)
    stamp_array = []
    for item in replies:
        stamp_array.append(str2stamp(item['time']))
    latest = max(stamp_array)
    distribution = [0]*N
    for item in stamp_array:
        index = int((item-created)/(latest+0.01-created) * N)
        distribution[index] += 1
    distribution = ','.join(str(i) for i in distribution)
    return distribution


def reply_sex_distribution(replies):
    male = 0
    female = 0
    unknown = 0
    for item in replies:
        if item['sex'] == '男':
            male += 1
        elif item['sex'] == '女':
            female += 1
        else:
            unknown += 1
    sex_distribution = str(male)+','+str(female)+','+str(unknown)
    return sex_distribution


def jieba_cut(text):
    cut = jieba.cut(text)
    words = ' '.join(cut)
    return words


def word_cloud(text, path):
    words = jieba_cut(text)
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    font_path = root_path + '/st.ttf'
    wc = WordCloud(
        font_path=font_path,
        background_color='black',
        width=600,
        height=300,
        prefer_horizontal=0.7,
        max_words=100,
        colormap='hsv',
        min_font_size=6
        ).generate(words)
    wc.to_file(path)
