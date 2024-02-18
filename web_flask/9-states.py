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


@app.route('/states', strict_slashes=False)
def states():
    """
    Display a HTML page with a list of all State objects present in DBStorage
    """
    states = storage.all("State").values()
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_by_id(id):
    """
    Display a HTML page with the list of City objects linked to the State
    """
    state = storage.get("State", id)
    if state:
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html', not_found=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
