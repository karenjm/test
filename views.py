import actions
from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return "Hello, I'm DevOps Anywhere"


@app.route('/keywords/<text>', methods=['GET', 'POST'])
def recv_keywords(text):

    if 'trident' in text or 'build' in text:
        actions.start_trident_build()
        return "Build Started"

    if 'status' in text:
        if actions.has_build_in_queue():
            return "Build is pending"
        number, url = actions.get_trident_last_build()
        return "Build is " + actions.get_trident_build_result(number)

