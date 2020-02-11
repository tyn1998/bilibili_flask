import binascii             # 用于暴力破解加密后的弹幕发送者uid
import time                 # 用于将时间戳转换成正常格式


def uid_decoder(hash_uid):
    for i in range(1, 100000000):
        if binascii.crc32(str(i).encode("utf-8")) == int(hash_uid, 16):
            uid = i
            return uid


def time_reformat(time_stamp):
    time_array = time.localtime(time_stamp)
    new_form = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return new_form
