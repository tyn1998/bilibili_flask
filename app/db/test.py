from app import app
from flask import current_app
from app.api.views import bilibilier_info


with app.app_context():
    print(bilibilier_info('4085626'))
