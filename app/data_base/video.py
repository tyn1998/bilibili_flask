from app import fetch_data
from app.data_base.DB import DB

db = DB(passwd='TYn13646825688', db='bilibili_flask')


def delete(av):
    sql1 = 'delete from v_basic where av = %s'
    sql2 = 'delete from v_tags where av = %s'
    sql3 = 'delete from v_replies where av = %s'
    sql4 = 'delete from v_subreplies where av = %s'
    sql5 = 'delete from v_danmus where av = %s'
    params = (av,)
    with db as cur:
        try:
            cur.execute(sql1, params)
            cur.execute(sql2, params)
            cur.execute(sql3, params)
            cur.execute(sql4, params)
            cur.execute(sql5, params)
            db.conn.commit()
        except Exception as e:
            print(e)
            db.conn.rollback()


def write(av):
    v_info = fetch_data.video.video_info(av)

    # 先清除再写入
    delete(av)

    sql = 'insert into v_basic values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    params = (
        v_info['av'],
        v_info['title'],
        v_info['view'],
        v_info['like'],
        v_info['favorite'],
        v_info['coin'],
        v_info['share'],
        v_info['danmu_count'],
        v_info['reply_count'],
        v_info['description']
    )
    with db as cur:
        try:
            cur.execute(sql, params)
            db.conn.commit()
        except Exception as e:
            print(e)
            db.conn.rollback()

    for tag in v_info['tags']:
        sql = 'insert into v_tags values(%s,%s,%s)'
        params = (
            av,
            tag['tag_id'],
            tag['tag_name']
        )
        with db as cur:
            try:
                cur.execute(sql, params)
                db.conn.commit()
            except Exception as e:
                print(e)
                db.conn.rollback()

    for reply in v_info['replies']:
        sql = 'insert into v_replies values(%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (
            reply['rpid'],
            av,
            reply['content'],
            reply['time'],
            reply['uid'],
            reply['uname'],
            reply['sex'],
            reply['like'],
        )
        with db as cur:
            try:
                cur.execute(sql, params)
                db.conn.commit()
            except Exception as e:
                print(e)
                db.conn.rollback()

        if len(reply['sub_replies']) != 0:
            for sub_reply in reply['sub_replies']:
                sql = 'insert into v_subreplies values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                params = (
                    sub_reply['rpid'],
                    sub_reply['root'],
                    sub_reply['parent'],
                    sub_reply['dialog'],
                    av,
                    sub_reply['content'],
                    sub_reply['time'],
                    sub_reply['uid'],
                    sub_reply['uname'],
                    sub_reply['sex'],
                    sub_reply['like'],
                )
                with db as cur:
                    try:
                        cur.execute(sql, params)
                        db.conn.commit()
                    except Exception as e:
                        print(e)
                        db.conn.rollback()
        else:
            pass

    for danmu in v_info['danmus']:
        sql = 'insert into v_danmus values(%s,%s,%s,%s,%s)'
        params = (
            av,
            danmu['time'],
            danmu['beijing_time'],
            danmu['coded_uid'],
            danmu['content'],
        )
        with db as cur:
            try:
                cur.execute(sql, params)
                db.conn.commit()
            except Exception as e:
                print(e)
                db.conn.rollback()


def read(av):
    info = {}

    sql = 'select * from v_basic where av = %s'
    params = (av,)
    with db as cur:
        try:
            cur.execute(sql, params)
            result = cur.fetchone()
            info['av'] = result['av']
            info['title'] = result['title']
            info['view'] = result['view_count']
            info['like'] = result['like_count']
            info['favorite'] = result['favorite_count']
            info['coin'] = result['coin_count']
            info['share'] = result['share_count']
            info['danmu_count'] = result['danmu_count']
            info['reply_count'] = result['reply_count']
            info['description'] = result['des']
        except Exception as e:
            print(e)

    tags = []
    sql = 'select * from v_tags where av = %s'
    params = (av,)
    with db as cur:
        try:
            cur.execute(sql, params)
            for item in cur.fetchall():
                tag = {
                    'tag_id': item['tag_id'],
                    'tag_name': item['tag_name'],
                }
                tags.append(tag)
        except Exception as e:
            print(e)
    info['tags'] = tags

    replies = []
    sql = 'select * from v_replies where av = %s'
    params = (av,)
    with db as cur:
        try:
            cur.execute(sql, params)
            for item in cur.fetchall():
                sub_replies = []
                sql = 'select * from v_subreplies where av = %s and root = %s'
                params = (av, item['rpid'])
                temp_db = DB(passwd='TYn13646825688', db='bilibili_flask')
                with temp_db as sub_cur:
                    try:
                        sub_cur.execute(sql, params)
                        for sub_item in sub_cur.fetchall():
                            sub_reply = {
                                'rpid': sub_item['rpid'],
                                'root': sub_item['root'],
                                'parent': sub_item['parent'],
                                'dialog': sub_item['dialog'],
                                'content': sub_item['content'],
                                'time': sub_item['bj_time'],
                                'uid': sub_item['uid'],
                                'umame': sub_item['uname'],
                                'sex': sub_item['sex'],
                                'like': sub_item['like_count']
                            }
                            sub_replies.append(sub_reply)
                    except Exception as e:
                        print(e)

                reply = {
                    'rpid': item['rpid'],
                    'content': item['content'],
                    'time': item['bj_time'],
                    'uid': item['uid'],
                    'umame': item['uname'],
                    'sex': item['sex'],
                    'like': item['like_count'],
                    'sub_replies': sub_replies
                }
                replies.append(reply)
        except Exception as e:
            print(e)
    info['replies'] = replies

    danmus = []
    sql = 'select * from v_danmus where av = %s'
    params = (av,)
    with db as cur:
        try:
            cur.execute(sql, params)
            for item in cur.fetchall():
                danmu = {
                    'time': item['v_time'],
                    'beijing_time': item['bj_time'],
                    'coded_uid': item['coded_uid'],
                    'content': item['content'],
                }
                danmus.append(danmu)
        except Exception as e:
            print(e)
    info['danmus'] = danmus

    return info