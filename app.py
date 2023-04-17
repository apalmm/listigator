from flask import render_template, request, session, redirect, url_for, make_response
from models import User, List, Lawyer
from database import db, get_lawyers
from flask import Blueprint
from auth import login_required

from constants import field_options

# create the app
main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    """Displays search form and results table"""
    return redirect(url_for('auth.login'))

@main.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('main/home.html', field_options=field_options)

@main.route('/search')
def results():
    name = request.args.get('name')
    city = request.args.get('city')
    phone = request.args.get('phone')
    field = request.args.get('field')
    
    print(name, city, phone, field)
    
    if name == "" and city == "" and phone == "":
        html = ""
    else:
        lawyers = get_lawyers(name, city, phone, field)
        html = render_template('main/results.html', lawyers=lawyers)

    return make_response(html)

@main.route('/create', methods=['POST'])
def create():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        lawyers = request.json
        
        user_id = session.get('user_id')
        
        list = List('Dummy_Title')
        user = User.query.get(user_id)
        
        user.lists.append(list)
        
        for lawyer in lawyers:
            lawyer = Lawyer(lawyer['city'], lawyer['field'], lawyer['license'], lawyer['name'], lawyer['phone'], 'blah')
            list.lawyers.append(lawyer)
        
        db.session.add(list)
        db.session.commit()
        
        return lawyers
    else:
        return 'Content-Type not supported!'
