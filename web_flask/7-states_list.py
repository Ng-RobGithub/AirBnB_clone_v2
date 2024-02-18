#!/usr/bin/python3
"""
Starts a Flask web application
"""

from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """After each request you must remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    Display a HTML page with a list of all State objects present in DBStorage
    """

    states = storage.all("State").values()
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
