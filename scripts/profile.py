from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_required, current_user

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from models import db, Users

profile = Blueprint('profile', __name__, template_folder='../templates')
login_manager = LoginManager()
login_manager.init_app(profile)

@profile.route('/profile', methods=['GET', 'POST'])
@login_required
def show():
    if 'new-password' in request.form and request.method == 'POST':
            username = request.form['username']
            password = request.form['current-password']
            newPassword = request.form['new-password']
            confirmPassword = request.form['confirm-password']

            user = Users.query.filter_by(username=username).first()

            if not check_password_hash(user.password, password):
                    flash('Passwords don\'t match.', 'error')
                    return redirect(url_for('profile.show') + '?error=passwords-dont-match')
            if newPassword != confirmPassword:
                flash('Incorrect password.', 'error')
                return redirect(url_for('profile.show') + '?error=password-dont-match')

            hashedPassword = generate_password_hash(newPassword, method='sha256')
            user.password = hashedPassword
            db.session.commit()
            flash('Password successfully changed')
    elif 'new-username' in request.form and request.method == 'POST':
        username = request.form['username']
        newUsername = request.form['new-username']
        password = request.form['current-password']

        user = Users.query.filter_by(username=username).first()

        if not check_password_hash(user.password, password):
            flash('Passwords don\'t match.', 'error')
            return redirect(url_for('profile.show') + '?error=passwords-dont-match')

        user.username = newUsername
        db.session.commit()
        flash('Username successfully changed')
    elif 'delete-account' in request.form:
        username = request.form['username']
        Users.query.filter_by(username=username).delete()

        return render_template('login.html')


    status_list = [['Online', '#43b581'], ['Idle', '#faa61a'], ['Offline', '#99aab5']]

    return render_template('profile.html', status_list=status_list)