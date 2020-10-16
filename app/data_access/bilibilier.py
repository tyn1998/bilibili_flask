from app.data_fetch import bilibilier
from app.data_access import video
from app.data_access.DB import DB
from datetime import datetime

db = DB(passwd='你的密码', db='bilibili_flask')


def delete(uid):
    sql1 = 'delete from bilibiliers where uid = %s'
    sql2 = 'delete from videos where uid = %s'
    params = (uid,)
    db.execute(sql1, params)
    db.execute(sql2, params)


def write(uid):
    b = bilibilier.bilibilier_info(uid)

    # 先清除再写入
    delete(uid)

    sql = 'insert into bilibiliers values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    params = (
        b['uid'],
        b['name'],
        b['sex'],
        b['birthday'],
        b['sign'],
        b['face_photo_url'],
        b['top_photo_url'],
        b['following'],
        b['follower'],
        b['video_count']
    )
    db.execute(sql, params)

    for video in b['videos']:
        sql = 'insert into videos values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        if video['play'] == '--':
            video['play'] = -1
        params = (
            video['av'],
            b['uid'],
            video['title'],
            video['description'],
            video['length'],
            video['created'],
            video['play'],
            video['comment'],
            video['pic'],
        )
        db.execute(sql, params)


def read(uid):
    info = {}

    sql = 'select * from bilibiliers where uid = %s'
    params = (uid,)
    try:
        result = db.execute(sql, params)[0]
        info['uid'] = result['uid']
        info['name'] = result['uname']
        info['sex'] = result['sex']
        info['birthday'] = result['birthday']
        info['sign'] = result['sign']
        info['face_photo_url'] = result['face_photo_url']
        info['top_photo_url'] = result['top_photo_url']
        info['following'] = result['following_count']
        info['follower'] = result['follower_count']
        info['video_count'] = result['video_count']
    except Exception as e:
        print(e)

    videos = []
    sql = 'select * from videos where uid = %s'
    params = (uid,)
    try:
        result = db.execute(sql, params)
        for item in result:
            video = {
                'av': item['av'],
                'title': item['title'],
                'description': item['des'],
                'length': item['length'],
                'created': item['created'],
                'play': item['play_count'],
                'comment': item['comment_count'],
                'pic': item['cover_photo_url']
            }
            videos.append(video)
    except Exception as e:
        print(e)

    info['videos'] = videos
    return info


def write_all_videos(uid):
    b = read(uid)
    for item in b['videos']:
        try:
            video.write(item['av'])
        except Exception as e:
            print(e)


def write_remained_videos(uid):
    b = read(uid)
    try:
        sql = 'select av from v_basic where av in (select av from videos where uid = %s)' % uid
        result = db.execute(sql)
        for item in b['videos']:
            tmp = {'av': item['av']}
            if tmp not in result:
                try:
                    video.write(item['av'])
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


def read_comprehensive(uid):
    sql = 'select * from bilibiliers where uid = %s' % uid
    b = db.execute(sql)[0]
    sql = 'select * from v_basic where av in (select av from videos where uid = %s)' % uid
    v = db.execute(sql)
    b_comprehensive = {
        'uid': b['uid'],
        'uname': b['uname'],
        'sex': b['sex'],
        'birthday': b['birthday'],
        'sign': b['sign'],
        'face_photo_url': b['face_photo_url'],
        'top_photo_url': b['top_photo_url'],
        'following_count': b['following_count'],
        'follower_count': b['follower_count'],
        'video_count': b['video_count'],
        'v_basic': v
    }
    return b_comprehensive


def build_all_continue(uid):
    print('--------------- buid(%s) ---------------' % uid)
    print(datetime.now(), '*** write(%s)' % uid)
    write(uid)
    print(datetime.now(), '#')
    print(datetime.now(), '*** read(%s)' % uid)
    b = read(uid)
    print(datetime.now(), '#')
    try:
        print(datetime.now(), '*** select av from v_basic')
        sql = 'select av from v_basic where av in (select av from videos where uid = %s)' % uid
        result = db.execute(sql)
        print(datetime.now(), '#')
        for i,item in enumerate(b['videos']):
            tmp = {'av': item['av']}
            # tmp = {'av': '0'}
            if tmp not in result:
                try:
                    print('进度：[%d/%d]' % (i+1,len(b['videos'])))
                    print(datetime.now(), '*** write(%s)' % item['av'])
                    video.write(item['av'])
                    print(datetime.now(), '#')
                    print(datetime.now(), '*** write_comprehensive(%s)' % item['av'])
                    video.write_comprehensive(item['av'])
                    print(datetime.now(), '#')
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)


def all_bilibiliers():
    sql = 'select uid from bilibiliers'
    result = db.execute(sql)
    return result
