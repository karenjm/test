import json

from flask import Flask

import actions
from text import FuzzyMatching

app = Flask(__name__)


TEMPLATE_FILE = 'text/templates.json'


def load_templates(template_json):
    with open(template_json, "r") as f:
        template_data = json.load(f)
        templates_build = template_data["templates_build"]
        templates_status = template_data["templates_status"]
        return templates_build, templates_status


@app.route('/')
@app.route('/index')
def index():
    return "Hello, I'm DevOps Anywhere"


@app.errorhandler(404)
def error_404(error_code):
    return "Sorry, I could not understand what I should do for you."


templates_build, templates_status = load_templates(TEMPLATE_FILE)


@app.route('/keywords/<text>', methods=['GET', 'POST'])
def recv_keywords(text):

    fuzzy_matching = FuzzyMatching(templates_build, templates_status, text)
    result = fuzzy_matching.text_analyzed()

    if result == 'build':
        actions.start_trident_build()
    elif result == 'status':
        if actions.has_build_in_queue():
            return "Build is pending"
        number, url = actions.get_trident_last_build()
        result = actions.get_trident_build_result(number)
        if result:
            return "Build Complete with {}".format(result)
        else:
            return "Build is in progress"
    else:
        if 'trident' in text or 'build' in text:
            actions.start_trident_build()
            return "Build Started"

        if 'status' in text:
            if actions.has_build_in_queue():
                return "Build is pending"
            number, url = actions.get_trident_last_build()
            result = actions.get_trident_build_result(number)
            if result:
                return "Build Complete with {}".format(result)
            else:
                return "Build is in progress"

    return "Sorry, I could not understand what I should do for you."
