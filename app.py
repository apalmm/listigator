from flask import Flask, render_template, request, redirect, url_for, make_response
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from models import User, List, Lawyer
from database import db, get_lawyers
from constants import field_options

# create the app
app = Flask(__name__)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///listigator.sqlite3"

# initialize the app with the extension
db.init_app(app)

@app.route('/', methods=['GET'])
def index():
    """Displays search form and results table"""
    return redirect('login')

@app.route('/register',methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if (request.form['password'] == request.form['confirm_password']):
            user = User(username, request.form['password'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, request.form['password']):
                return redirect(url_for('home'))
            else:
                message = 'Invalid login information.'
        else:
            message = 'Missing login information.'
            
    return render_template('login.html', message=message)

@app.route('/home', methods = ['POST', 'GET'])
def home():
    return render_template('home.html', field_options=field_options)

@app.route('/search')
def results():
    name = request.args.get('name')
    city = request.args.get('city')
    phone = request.args.get('phone')
    
    print(name, city, phone)
    
    if name == "" and city == "" and phone == "":
        html = ""
    else:
        lawyers = get_lawyers(name, city, phone)
        html = render_template('results.html', lawyers=lawyers)

    return make_response(html)

if __name__ == '__main__':
    app.run(debug=True)
