from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # 🔁 Move imports here to avoid circular dependency
    from app.models import User, Setting, Module

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_globals():
        modules = Module.query.all()
        user = User.query.get(session.get('id')) if session.get('id') else None
        user_modules = user.role.modules if user and user.role else []

        settings = {s.function_desc: s.function for s in Setting.query.all()}
        return dict(modules=modules, user_modules=user_modules, settings=settings)

    from app.routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
