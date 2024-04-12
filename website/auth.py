from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Quote
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user
from .pricing_module import PricingModule

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
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

            hashed_password = generate_password_hash(password1)
            new_user = User(username = username, password = hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("client_registration.html", user=current_user)

# Profile Management path
@auth.route('/profile_management', methods=['GET', 'POST'])
@login_required
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
@login_required
def quoteform():
    address = current_user.address1
    if current_user.address2:
        address += ", {}".format(current_user.address2)
    address += "{}, {}, {}".format(current_user.city, current_user.state, current_user.zipcode)
    if request.method == 'POST':
        gallons = request.form.get('gallons')
        date = request.form.get('date')
        price = None
        total = None
        if not gallons and not date:
            flash('Enter an amount for fuel voluem (gallons) and choose a delivery date', category='error')
        elif not gallons:
            flash('Enter an amount for fuel volume (gallons)', category='error')
        elif not date:
            flash('Choose a delivery date', category='error')
        elif not address:
            flash('Save your delivery address in Profile Management', category='success')
        else:
            gallons = float(gallons)
            price = PricingModule(address)
            total = gallons * price
            new_quote = Quote(user_id=current_user.id, gallons=gallons, address=address, date=date, price=price, total=total)
            db.session.add(new_quote)
            db.session.commit()
            price = f'${price:.2f}'
            total = f'${total:.2f}'
            flash('Fuel Quote Submitted!', category='success')
        return render_template('quoteform.html', user=current_user, price=price, total=total, gallons=gallons, date=date, address=address)
    return render_template('quoteform.html', user=current_user, address=address)

@auth.route('/history', methods=['GET'])
@login_required

def history():
    quotes = current_user.quotes
    if current_user.quotes:
        quotes = current_user.quotes
        return render_template('history.html', user=current_user, quotes=quotes)
    else:
        message = "No client quote history exists"
    return render_template('history.html', user=current_user, message=message)