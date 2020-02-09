from flask import Blueprint

api = Blueprint('api', __name__)

from . import test_views
from . import bilibilier_info
