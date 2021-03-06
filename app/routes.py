import os
import time
import hashlib
from app import app, db, photos, avatars
from flask import render_template, get_flashed_messages, flash, redirect, url_for, request
from app.forms import *
from app.models import User
from wtforms import SubmitField
from flask_login import current_user, login_user, logout_user, login_required
from app.email import send_reset_password_mail
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')

@login_required
@app.route('/index', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        for filename in request.files.getlist('photo'):
            name = hashlib.md5(('admin' + str(time.time())).encode('UTF-8')).hexdigest()[:15]
            photos.save(filename, name=name + '.')
        flash('upload success', category="success")
    return render_template('index.html', form=form)

@login_required
@app.route('/manage')
def manage_file():
    files_list = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    return render_template('manage.html', files_list=files_list)


@app.route('/open/<filename>')
def open_file(filename):
    file_url = photos.url(filename) #获取文件的绝对路径
    flash('open success', category="info")
    return render_template('browser.html', file_url=file_url)


@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = photos.path(filename)
    os.remove(file_path)
    flash('delete success', category="info")
    return redirect(url_for('manage_file'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #判断用户是否成功输入了正确密码并且已经登录
        return redirect(url_for('upload_file'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Login success', category='info')
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect( next_page)
            return redirect(url_for('upload_file'))
        flash('User not exit or password not match', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('upload_file'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    if current_user.is_authenticated: #判断用户是否成功输入了正确密码并且已经登录
        return redirect(url_for('upload_file'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        token = user.get_reset_password_token()
        send_reset_password_mail(user=user, token=token)
        flash('Password reset request mail is sent, please check your mailbox', category='info')
    return render_template('send_password_reset_request.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('Upload_file'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.check_reset_password_token(token)
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your password reset is done, you can login with new password now.', category='info')
            return redirect(url_for('login'))
        else:
            flash('The user is not exits', category='info')
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.before_request #查看功能之前执行的装饰功能
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@login_required
@app.route('/edit-avatar', methods=['GET', 'POST'])
def change_avatar():
    form = UploadForm()
    if form.validate_on_submit():
        filename = avatars.save(form.photo.data)
        file_url = avatars.url(filename)
        current_user.avatar = file_url
        db.session.add(current_user)
        db.session.commit()
        flash('修改成功!')
        return redirect(url_for('user', username=current_user.username, file_url=file_url))
    return render_template('change_avatar.html',form=form, file_url=current_user.avatar)