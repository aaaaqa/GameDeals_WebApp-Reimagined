from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

import sqlalchemy

from models import db, Users

login = Blueprint('login', __name__, template_folder='../templates')
login_manager = LoginManager()
login_manager.init_app(login)

@login.route('/login', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home.show'))
            else:
                flash('Incorrect Password.', 'error')
                return redirect(url_for('login.show') + '?error=incorrect-password')
        else:
            flash('User not found.', 'error')
            return redirect(url_for('login.show') + '?error=user-not-found')
    else:
        return render_template('login.html')

register = Blueprint('register', __name__, template_folder='../templates')
login_manager = LoginManager()
login_manager.init_app(register)

@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(
                    password, method='sha256')
                try:
                    new_user = Users(
                        username=username,
                        email=email,
                        password=hashed_password,
                    )

                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    flash('User or Email already exists.', 'error')
                    return redirect(url_for('login.show') + '?error=user-or-email-exists')

                return redirect(url_for('home.show') + '?success=account-created')
            else:
                flash('Passwords must be same.', 'error')
                return redirect(url_for('login.show') + '?error=password-not-match')
        else:
            flash('Missing fields.', 'error')
            return redirect(url_for('login.show') + '?error=missing-fields')
    else:
        return render_template('login.html')