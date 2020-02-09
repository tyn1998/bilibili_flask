from . import api

@api.route('/')
def test():
    return '这是一个最精简的使用了蓝图的flask框架！'