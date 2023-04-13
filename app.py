from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import User, List, Lawyer
from database import db

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

@app.route('/login',methods = ['POST', 'GET'])
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

@app.route('/home',methods = ['POST', 'GET'])
def home():
    return render_template('home.html')

# @app.route('/results', methods=['POST'])
# def results():
#     field = request.form['field']
#     name = request.form['name']
#     city = request.form['city']
#     probono = request.form.get('probono')
#     phone = request.form['phone']

#     query = "SELECT * FROM Lawyer INNER JOIN Field ON Field.LicenseNumber=Lawyer.LicenseNumber"
#     parameters = {}
#     conditions = []

#     if field:
#         conditions.append("Field LIKE :field")
#         parameters['field'] = f'%{field}%'
#     if name:
#         conditions.append("Name LIKE :name")
#         parameters['name'] = f'%{name}%'
#     if city:
#         conditions.append("City LIKE :city")
#         parameters['city'] = f'%{city}%'
#     if probono is not None:
#         conditions.append("Status = 'Pro Bono'")
#         parameters['probono'] = probono
#     if phone:
#         conditions.append("Phone LIKE :phone")
#         parameters['phone'] = f'%{phone}%'
    
#     if conditions:
#         query += " WHERE " + " AND ".join(conditions)

#     with sqlite3.connect('WALawyers.sqlite') as conn:
#         cursor = conn.cursor()
#         results = cursor.execute(query, parameters).fetchall()

#     return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
