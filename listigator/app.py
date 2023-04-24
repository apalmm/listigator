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
    probono = request.form.get('status')
    
    print(name, city, phone, field, probono)
    
    if name == "" and city == "" and phone == "" and field == "":
        html = ""
    else:
        lawyers = get_lawyers(name, city, phone, field, probono)
        html = render_template('main/results.html', lawyers=lawyers)

    return make_response(html)

@main.route('/searchList', methods=["POST"])
def listSearch():
    if request.method == "POST":
        listname = request.form.get('searchTitle')

        if listname is not '':
            queryname = "%" + listname + "%"
            lists = db.session.query(List).filter(List.title.like(queryname), List.public==True)
            html = render_template('main/publiclists.html', lists=lists, querying=True)

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
        
        
        db.session.add(list)
        
        db.session.commit()
        
        
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
    public_lists = List.query.filter_by(public=True).join(User, List.user_id == User.id).all()
    return render_template('main/publiclists.html', lists=public_lists, querying=False)

@main.route('/delete/<int:list_id>')
@login_required
def delete(list_id):
    list_to_delete = List.query.get_or_404(list_id)
    try:
        db.session.delete(list_to_delete)
        db.session.commit()
        return redirect('/mylists')
    except:
        return "There was a problem deleting this list"

@main.route('/list/<int:list_id>')
@login_required
def list(list_id):
    list_to_show = List.query.get(list_id)
    lawyers = list_to_show.lawyers
    title = list_to_show.title
    return render_template('main/list.html', lawyers = lawyers, title=title)

@main.route('/user/<int:user_id>')
@login_required
def user(user_id):
    user_id = session.get('user_id')
    public_lists = List.query.filter_by(public=True).join(User, List.user_id == User.id).all()
    return render_template('main/user.html', lists=public_lists)

        
