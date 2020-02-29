from . import api
from app import fetch_data
from flask import jsonify, Response


@api.route('/bilibiliers/<string:uid>', methods=['GET'])
def bilibilier_info(uid):
    result = fetch_data.bilibilier.bilibilier_info(uid)
    return jsonify(result)


@api.route('/videos/<string:av>', methods=['GET'])
def video_info(av):
    result = fetch_data.video.video_info(av)
    return jsonify(result)

from app.functions import test_ciyu
@api.route('/ciyun/<string:av>', methods=['GET'])
def ciyun(av):
    bytes_image = test_ciyu.ciyun(av)
    res = Response(bytes_image, mimetype='image/png')
    return res
