import os
from . import api
from app import data_fetch
from flask import jsonify, Response
from app.data_access import video
from app.data_access import bilibilier
import shutil
from app.data_access.DB import DB


def init_directory():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    images_path = root_path + '/word_cloud_images/'
    if os.path.exists(images_path):
        shutil.rmtree(images_path)
    os.mkdir(root_path + '/word_cloud_images/')


@api.route('/bilibiliers/<string:uid>', methods=['GET'])
def bilibilier_info(uid):
    result = data_fetch.bilibilier.bilibilier_info(uid)
    return jsonify(result)


@api.route('/videos/<string:av>', methods=['GET'])
def video_info(av):
    result = data_fetch.video.video_info(av)
    return jsonify(result)


@api.route('/b_comprehensive/<string:uid>', methods=['GET'])
def b_comprehensive(uid):
    result = bilibilier.read_comprehensive(uid)
    return jsonify(result)


@api.route('/v_comprehensive/<string:av>', methods=['GET'])
def v_comprehensive(av):
    result = video.read_comprehensive(av)
    return jsonify(result)


@api.route('/ciyun_danmus/<string:av>', methods=['GET'])
def ciyun_danmus(av):
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    img_path = root_path + '/word_cloud_images/av%s_d.png' % av
    image = video.read_image_stream(img_path)
    return Response(image, mimetype='image/png')


@api.route('/ciyun_replies/<string:av>', methods=['GET'])
def ciyun_replies(av):
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir))
    img_path = root_path + '/word_cloud_images/av%s_r.png' % av
    image = video.read_image_stream(img_path)
    return Response(image, mimetype='image/png')


@api.route('/build_all/<string:uid>', methods=['GET'])
def build_all(uid):
    try:
        bilibilier.build_all_continue(uid)
        return jsonify({'status': 'success'})
    except Exception as e:
        print('>>@api.route(build_all)')
        print(e)
        return jsonify({'status': 'fail'})


@api.route('/init', methods=['GET'])
def init():
    init_directory()
    DB.reset()
    return jsonify({'status': 'success'})


@api.route('/all_bilibiliers', methods=['GET'])
def all_bilibiliers():
    result = bilibilier.all_bilibiliers()
    return jsonify(result)
