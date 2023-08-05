import os
from flask import Flask
import click

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'pool_log.sqlite'),
            )

    if test_config is None:
        # Load the instance configuration file
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed as an argument
        app.config.from_mapping(test_config)

    # Make sure the instant folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World!!!'

    from . import db
    db.init_app(app)

    from . import log, pool
    app.register_blueprint(log.bp)
    app.register_blueprint(pool.bp)
    app.add_url_rule('/', endpoint='index')

    return app

