from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #app.config.from_object(LocalDevelopmentConfig)
    # app.config['CACHE_TYPE']='redis'
    # app.config['CACHE_REDIS_HOST']='redis'
    # app.config['CACHE_REDIS_PORT']='6379'
    # app.config['CACHE_REDIS_DB']='0'
    # app.config['CACHE_REDIS_URL']='rediss://red-clvi1veg1b2c73cgrui0:50xxq9dgmrjgZBrbWyhu4jKoI6kQTFxn@oregon-redis.render.com:6379'
    # app.config['CACHE_DEFAULT_TIMEOUT']='500'
    # cache.init_app(app)

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.session.close_all()
    db.init_app(app)

    CORS(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    with app.app_context():
        db.create_all()

    return app
