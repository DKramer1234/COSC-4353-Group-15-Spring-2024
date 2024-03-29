from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('auth.profile_management')) # Redirecting to profile management for now
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/client_registration', methods=['GET', 'POST'])
def client_registration():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 3 characters.', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(
                password1)) ## IMPORTANT, NEED TO HASH THE PASSWORD. REMOVED HASH TO MAKE WORK.
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("client_registration.html", user=current_user)

# Profile Management path
@auth.route('/profile_management', methods=['GET', 'POST'])
def profile_management():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        # gets the form information and saves it

        if len(full_name) > 50:
            flash('Full name cannot be greater than 50 characters', category='error')
        elif len(address1) > 100:
            flash('Address 1 cannot be greater than 100 characters', category='error')
        elif len(address2) > 100:
            flash('Address 2 cannot be greater than 100 characters', category='error')
        elif len(city) > 100:
            flash('City cannot be greater than 100 characters', category='error')
        else:
            current_user.full_name = full_name
            current_user.address1 = address1
            current_user.address2 = address2
            current_user.city = city
            current_user.state = state
            current_user.zipcode = zipcode

        db.session.commit() # saves the changes in db
        flash('Profile information saved!', category='success')
        #return redirect(url_for('auth.profile_management')) 
    
    return render_template('profile_management.html', user=current_user)

@auth.route('/quoteform', methods=['GET', 'POST'])
def quoteform(): # will need login required eventually
    # TO DO: FUNCTION DEFINITION
    return render_template('quoteform.html', user=current_user)

@auth.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('history.html', user=current_user)