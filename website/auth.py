from flask import Blueprint
from .forms import LoginForm, SignUpForm, PasswordChangeForm
from flask import render_template
from .models import Customer
from . import db
from flask import flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data

        if password1 == password2:
            new_customer = Customer()
            new_customer.email = email
            new_customer.username = username
            new_customer.password = password1

            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account created successfully! You can now log in.')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account creation failed, email already exists')
            
            form.email.data = ''
            form.username.data = ''
            form.password1.data = ''
            form.password2.data = ''
         
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data 
        password = form.password.data

        customer = Customer.query.filter_by(email=email).first()

        if customer:
            if customer.verify_password(password = password):
                login_user(customer)
                print('Login successful')
                return redirect('/')
            else:
                flash('Incorrect password, please try again.')
        else:
            flash('Account does not exist, sign up to create account')

    return render_template('login.html', form=form) 


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth.route('/profile/<int:customer_id>')
@login_required
def profile(customer_id):
    print('Customer ID:', customer_id)
    customer = Customer.query.get(customer_id)
    return render_template('profile.html', customer=customer)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()

    return render_template('change_password.html', form=form)