from flask import Blueprint, render_template
from flask_login import LoginManager, login_required, current_user

from models import db

terms = Blueprint('terms', __name__, template_folder='../templates')
login_manager = LoginManager()
login_manager.init_app(terms)

@terms.route('/terms', methods=['GET'])
def show():
    return render_template('terms.html')