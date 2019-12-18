from flask import Flask
from .extensions import db, login_manager, bootstrap
from .commands import create_tables
from .models import User


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    bootstrap.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        from .routes import auth
        db.create_all()

    app.cli.add_command(create_tables)

    return app
