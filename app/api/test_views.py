from . import api
from flask import jsonify
from flask import request


@api.route('/', methods=['GET'])
def test():
    if request.method == 'GET':
        print('这是GET请求。')

    videos = [
        {
            'av': 1234567,
            'click': 100
        },
        {
            'av': 1234567,
            'click': 100
        }
    ]
    return jsonify({'videos': videos})

@api.route('/test_post', methods=['POST'])
def test_post():
    if request.method == 'POST':
        print('这是POST请求。')

    echo_json = {
        'av': request.form['av'],
        'click': request.form['click']
    }

    return jsonify(echo_json)