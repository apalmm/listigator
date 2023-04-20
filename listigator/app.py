from flask import render_template, request, session, redirect, url_for, make_response, Blueprint

from .database import db, get_lawyers
from .auth import login_required
from .models import User, List, Lawyer
from .constants import field_options

# create the app
main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    """Displays login screen"""
    return redirect(url_for('auth.login'))

@main.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    return render_template('main/home.html', field_options=field_options)

@main.route('/search')
@login_required
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
@login_required
def create():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        lawyers = request.json
        
        user_id = session.get('user_id')
        
        list = List(lawyers[1])
        user = User.query.get(user_id)
        
        user.lists.append(list)

        list.public = lawyers[2].get('public', False)
        for lawyer in lawyers[0]:
            lawyer = Lawyer(lawyer['city'], lawyer['field'], lawyer['license'], 
                            lawyer['name'], lawyer['phone'], 'blah')
            
            list.lawyers.append(lawyer)
        
        db.session.add(list)
        db.session.commit()
        
        return lawyers
    else:
        return 'Content-Type not supported!'

@main.route('/mylists')
@login_required
def mylists():
    user_id = session.get('user_id')
    user_id = User.query.get(user_id)
    lists = user_id.lists
    return render_template('main/mylists.html', lists=lists)

@main.route('/publiclists')
@login_required
def publiclists():
    public_lists = List.query.filter_by(is_public=True).all()
    return render_template('main/publiclists.html', lists=public_lists)