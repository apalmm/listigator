from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from werkzeug.security import check_password_hash
from models import User
from database import db
from flask import Blueprint
import functools

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST', 'GET'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if username and password and confirm_password:
            if (password == confirm_password):
                user = User(username, password)
                
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('auth.login'))
            else:
                message = 'Invalid register information.'
        else:
            message = 'Missing register information.'
        
    return render_template('auth/register.html', message=message)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, request.form['password']):
                session.clear()
                session['user_id'] = user.id
                
                return redirect(url_for('main.home'))
            else:
                message = 'Invalid login information.'
        else:
            message = 'Missing login information.'
            
    return render_template('auth/login.html', message=message)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(route):
    @functools.wraps(route)
    def wrapped_route(**kwargs):

        if session.get('user_id') is None:
            return redirect(url_for('auth.login'))
        else:
            print('hello!')
            print(session.get('user_id'))

        return route(**kwargs)

    return wrapped_route
