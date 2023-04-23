from flask import Flask   

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev', SQLALCHEMY_DATABASE_URI='sqlite:///listigator.sqlite3')
    # configure the SQLite database, relative to the app instance folder
    
    from database import db
    db.init_app(app)
    
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from app import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    app.add_url_rule('/', endpoint='index')

    return app