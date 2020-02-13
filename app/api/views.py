from . import api
from app import fetch_data
from flask import jsonify


@api.route('/bilibiliers/<string:uid>', methods=['GET'])
def bilibilier_info(uid):
    result = fetch_data.bilibilier.bilibilier_info(uid)
    return jsonify(result)


@api.route('/videos/<string:av>', methods=['GET'])
def video_info(av):
    result = fetch_data.video.video_info(av)
    return jsonify(result)
