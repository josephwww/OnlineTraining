import os

from flask import render_template, send_from_directory, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from Course import app, db, bcrypt
from Course.forms import LoginForm
from Course.models import User, Question, Test, Class

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@app.route('/class')
@login_required
def classs():
    return render_template('class.html', title='Class')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check your password', 'danger')
        flash('Login Unsuccessful. Username does not exist', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

#
# @app.route("/rating/<int:rating_id>/delete", methods=['POST'])
# @login_required
# def delete_rating(rating_id):
#     rating = Rating.query.get_or_404(rating_id)
#     if rating.author != current_user:
#         abort(403)
#     db.session.delete(rating)
#     db.session.commit()
#     flash('Vote has been deleted', 'success')
#     update_demography(current_user)
#     return redirect(url_for('result'))


@app.route("/class/<int:class_id>", methods=['GET'])
@login_required
def get_class(class_id):
    c = Class.query.get_or_404(class_id)
    if current_user not in c.students or current_user.role != 'admin':
        abort(403)

    return render_template('admin.html', title='admin')


@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.role != 'admin':
        abort(403)
    return render_template('admin.html', title='admin')