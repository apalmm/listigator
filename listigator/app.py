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
        data = request.json
        print(data)
        lawyers = data[0]

        title = data[1]

        is_public = data[2]


        user_id = session.get('user_id')
        user = User.query.get(user_id)
        
        list = List(title=title)
        list.public = is_public
        user.lists.append(list)

        for lawyer in lawyers:
            lawyer = Lawyer(lawyer['name'], lawyer['city'], lawyer['field'], 
                            lawyer['phone'], lawyer['license'], lawyer['status'])
            
            list.lawyers.append(lawyer)
        
        print("Made it to the db.session.add(list) line")
        db.session.add(list)
        print("Made it to the db.session.commit() line")
        db.session.commit()
        print("Made it PAST the db.session.commit() line")
        
        return data
    else:
        return 'Content-Type not supported!'

@main.route('/mylists')
@login_required
def mylists():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    lists = user.lists
    return render_template('main/mylists.html', lists=lists)

@main.route('/publiclists')
@login_required
def publiclists():
    public_lists = List.query.filter_by(public=True).all()
    return render_template('main/publiclists.html', lists=public_lists)
