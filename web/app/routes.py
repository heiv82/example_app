from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request


from app import app, db


from app.forms import LoginForm, RegistrationUserForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Device
from werkzeug.urls import url_parse
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    q = request.args.get('q')

    if q:
        devices = Device.query.filter(Device.device_name.contains(q) | Device.device_EUI.contains(q)).all()
    else:
        devices = Device.query.all()
    return render_template('service/index.html', title='Home', devices=devices)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('service.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('service.index')
        return redirect(next_page)
    
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('service.index'))


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        return redirect(url_for('service.index'))

    form = RegistrationUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    api_token=form.api_token.data)
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
        except:
            flash("Failed to save the new user")
        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))
    return render_template('register_user.html', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    devices = Device.query.filter_by(user=user)

    return render_template('user.html', user=user, devices=devices)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():

    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()

        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)


# Write last seen time
@app.before_request
def before_request():

    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# Clear browsers cache
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.cache_control.no_store = True
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
