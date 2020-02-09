from flask import Flask

app = Flask(__name__)

# 防止jsonify自动按字母表顺序排序
app.config['JSON_SORT_KEYS'] = False

from .api import api as api_blueprint

app.register_blueprint(api_blueprint, url_prefix='/api')
