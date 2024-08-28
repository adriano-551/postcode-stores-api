from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    from .api.v1 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
