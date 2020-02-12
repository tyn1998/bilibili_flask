import requests
from app.data_collector import assistance
from xml.etree import ElementTree


def video_info(av):
    r1 = requests.get('http://api.bilibili.com/archive_stat/stat', params={'aid': av})
    r2 = requests.get('https://api.bilibili.com/x/web-interface/view', params={'aid': av})
    r3 = requests.get('https://api.bilibili.com/x/tag/archive/tags', params={'aid': av})
    json_r1 = r1.json()
    json_r2 = r2.json()

    """
        r3访问官方标签api
    """
    json_r3 = r3.json()
    tags = []
    for item in json_r3['data']:
        tag = {
            'tag_id': item['tag_id'],
            'tag_name': item['tag_name'],
        }
        tags.append(tag)

    """
        r4访问官方弹幕api
        返回结果为XML文件
        需要专门处理
    """
    r4 = requests.get('https://api.bilibili.com/x/v1/dm/list.so', params={'oid': json_r2['data']['cid']})
    root = ElementTree.fromstring(r4.content)
    danmus = []
    for item in root.findall('d'):
        attributes = item.attrib['p'].split(',')
        danmu = {
            'time': attributes[0],
            'beijing_time': assistance.time_reformat(int(attributes[4])),
            'coded_uid': attributes[6],
            'content': item.text
        }
        danmus.append(danmu)

    """
        r5访问官方评论api
        评论里还有子评论
    """
    url = 'http://api.bilibili.com/x/v2/reply'
    params = {
        'oid': av,
        'pn': 1,
        'type': 1
    }
    replies = []
    while True:
        r5 = requests.get(url, params=params)
        json_r5 = r5.json()

        rlist = json_r5['data']['replies']
        for item in rlist:
            sub_replies = []
            if item['replies'] is None:
                pass
            else:
                for sub_item in item['replies']:
                    sub_reply = {
                        'rpid': sub_item['rpid'],
                        'root': sub_item['root'],
                        'parent': sub_item['parent'],
                        'dialog': sub_item['dialog'],
                        'content': sub_item['content']['message'],
                        'time': assistance.time_reformat(sub_item['ctime']),
                        'uid': sub_item['member']['mid'],
                        'uname': sub_item['member']['uname'],
                        'sex': sub_item['member']['sex'],
                        'like': sub_item['like']
                    }
                    sub_replies.append(sub_reply)

            r = {
                'rpid': item['rpid'],
                'content': item['content']['message'],
                'time': assistance.time_reformat(item['ctime']),
                'uid': item['member']['mid'],
                'uname': item['member']['uname'],
                'sex': item['member']['sex'],
                'like': item['like'],
                'sub_replies': sub_replies
            }
            replies.append(r)

        # 判断是否还有下一页
        page_info = json_r5['data']['page']
        if page_info['num'] * page_info['size'] > page_info['count']:
            break
        else:
            params['pn'] = params['pn'] + 1

    info = {
        'av': json_r1['data']['aid'],
        'title': json_r2['data']['title'],
        'view': json_r1['data']['view'],
        'like': json_r1['data']['like'],
        'favorite': json_r1['data']['favorite'],
        'coin': json_r1['data']['coin'],
        'share': json_r1['data']['share'],
        'danmu_count': json_r1['data']['danmaku'],
        'reply_count': json_r1['data']['reply'],
        'description': json_r2['data']['desc'],
        'tags': tags,
        'replies': replies,
        'danmus': danmus
    }
    return info
