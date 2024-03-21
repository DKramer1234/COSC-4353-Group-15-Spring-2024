from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
#from pricing_module import PricingModule

def PricingModule(delivery_address):
    # FUNCTION STUB: WILL BE COMPLETE FOR LAST ASSIGNMENT
    price_per_gal = 120.50 # units: $ / gal
    return price_per_gal

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
    return render_template('profile_management.html', user=current_user)

@auth.route('/quoteform', methods=['GET', 'POST'])
def quoteform(): # will need login required eventually
    # TO DO: FUNCTION DEFINITION
    if request.method == 'POST':
        gallons = float(request.form.get('gallons'))
        delivery_address = request.form.get('address') # address will be taken from db
        date = request.form.get('date')
        price = PricingModule(delivery_address)
        total = gallons * price
        flash('Fuel Quote Submitted!', category='success')
        return render_template('quoteform.html', user=current_user, price=price, total=total, gallons=gallons, date=date)
        # new_quote = Quote(gallons=gallons, address=delivery_address, data=date, price=price, total=total) <- what we might use to add this completed quote to the database
    return render_template('quoteform.html', user=current_user)

@auth.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('history.html', user=current_user)