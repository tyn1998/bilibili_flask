from app.fetch_data import bilibilier
from app.data_base import video
from app.data_base.DB import DB

db = DB(passwd='TYn13646825688', db='bilibili_flask')


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

