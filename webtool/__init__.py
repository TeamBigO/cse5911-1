from flask import Flask

def create_app():
    # name of the file ?
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'brianchrisliamsarah'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
