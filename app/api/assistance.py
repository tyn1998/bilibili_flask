# 用于暴力破解加密后的弹幕发送者uid
import binascii


def decode_uid(decoded_uid):
    for i in range(1, 100000000):
        if binascii.crc32(str(i).encode("utf-8")) == int(decoded_uid, 16):
            return i
