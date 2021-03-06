import requests
from app.data_fetch import assistance
import datetime


def bilibilier_info(uid):
    print('----------------------  fetching ', uid, '  -------------------------')
    r1 = requests.get('https://api.bilibili.com/x/space/acc/info', params={'mid': uid})
    """
        r2的api返回总播放数和总赞数
        在外部测试时，这个api正常返回结果
        在这里，状态码是4XX，无解
    """
    # r2 = requests.get('https://api.bilibili.com/x/space/upstat', params={'mid': uid})
    r3 = requests.get('https://api.bilibili.com/x/relation/stat', params={'vmid': uid})

    json_r1 = r1.json()
    json_r3 = r3.json()

    info = {
        'uid': json_r1['data']['mid'],
        'name': json_r1['data']['name'],
        'sex': json_r1['data']['sex'],
        'birthday': json_r1['data']['birthday'],
        'sign': json_r1['data']['sign'],
        'face_photo_url': json_r1['data']['face'],
        'top_photo_url': json_r1['data']['top_photo'],
        'following': json_r3['data']['following'],
        'follower': json_r3['data']['follower'],
    }

    url = 'https://api.bilibili.com/x/space/arc/search'
    params = {
        'mid': uid,
        'ps': 30,
        'tid': 0,
        'pn': 1,
        'keyword': '',
        'order': 'pubdate'
    }
    videos = []
    while True:
        r4 = requests.get(url, params=params)
        json_r4 = r4.json()

        vlist = json_r4['data']['list']['vlist']
        for item in vlist:
            v = {
                'av': item['aid'],
                'title': item['title'],
                'description': item['description'],
                'length': item['length'],
                'created': assistance.time_reformat(item['created']),
                'play': item['play'],
                'comment': item['comment'],
                'pic': item['pic']
            }
            videos.append(v)

        # 判断是否还有下一页
        page_info = json_r4['data']['page']
        if page_info['pn'] * page_info['ps'] > page_info['count']:
            break
        else:
            params['pn'] = params['pn'] + 1

    info['video_count'] = page_info['count']
    info['videos'] = videos

    print('[%s fetched]' % datetime.datetime.now())
    return info
