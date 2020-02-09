from flask import Flask
from flask_cors import *

app = Flask(__name__)

# 防止jsonify自动按字母表顺序排序
app.config['JSON_SORT_KEYS'] = False

# 解决跨域
CORS(app, supports_credentials=True)

from .api import api as api_blueprint

app.register_blueprint(api_blueprint, url_prefix='/api')
