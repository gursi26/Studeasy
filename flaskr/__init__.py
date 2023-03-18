import os
# flask --app hello run
# flask --app flaskr run --debug

# {{ url_for('static', filename='style.css') }}
# {{ url_for('static', filename='script.js') }}

from flask import Flask, render_template, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    app.static_folder = 'static'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/notegen')
    def notegen():
        return render_template('notegen.html')

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route("/notegen", methods=['POST'])
    def move_forward():
        if request.form['username']:
            prompt_req = request.form['username']
            
            return render_template('notegen.html', forward_message=forward_message)
        else:
            return render_template('notegen.html')

    return app
