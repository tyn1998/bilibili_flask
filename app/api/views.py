from . import api
from app import data_collector
from flask import jsonify


@api.route('/bilibiliers/<string:uid>', methods=['GET'])
def bilibilier_info(uid):
    result = data_collector.bilibilier.bilibilier_info(uid)
    return jsonify(result)


@api.route('/videos/<string:av>', methods=['GET'])
def video_info(av):
    result = data_collector.video.video_info(av)
    return jsonify(result)
