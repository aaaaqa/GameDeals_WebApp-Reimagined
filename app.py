import sqlalchemy
from flask_login import LoginManager
from flask import Flask,render_template, request , redirect,url_for
from werkzeug.routing import Rule

import sys

sys.path.insert(0, './scripts/')

from models import db, Users

from login import login, register
from logout import logout
from home import home
from profile import profile
from catalog import catalog
from terms import terms

app = Flask(__name__, static_folder='./templates/static')

@app.endpoint("catch_all")
def _404(_404):
    return render_template('login.html')

app.url_map.add(Rule("/", defaults={"_404": ""}, endpoint="catch_all"))

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../scripts/database.db'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()

with app.app_context():
    db.create_all()

app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(logout)
app.register_blueprint(home)
app.register_blueprint(profile)
app.register_blueprint(catalog)
app.register_blueprint(terms)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)