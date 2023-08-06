import os
from datetime import timedelta
from flask import Flask, session

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

    # Jinja filter that takes in a python datetime and uses the javascript UTC offset stored in the session to display the local time
    @app.template_filter('localtime')
    def local_time(time):
        if 'offset' in session:
            minutes = -float(session['offset'])
            tz_offset = timedelta(minutes=minutes)
            local_time = time + tz_offset
            return local_time
        else:
            return time
    
    # Jinja filter that takes in a python datetime and outputs a prettier string
    @app.template_filter('prettytime')
    def format_time(time):
        return time.strftime('%a %b %d, %I:%M %p') 

    from . import db
    db.init_app(app)

    from . import log, pool
    app.register_blueprint(log.bp)
    app.register_blueprint(pool.bp)
    app.add_url_rule('/', endpoint='index')

    return app

