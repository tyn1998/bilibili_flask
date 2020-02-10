from flask import Blueprint

api = Blueprint('api', __name__)

from . import bilibilier_info
from . import video_info
