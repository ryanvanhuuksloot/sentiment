from flask import Flask, g, jsonify, abort
from flask import render_template
from http import HTTPStatus
import jinja2

from classes.sentiment.sentimentClass import sentimentClass
from classes.auth.yaml import Yaml

api_keys = Yaml().readYaml('keys.yaml')
sources = ['abc-news', 'al-jazeera-english', 'cnbc', 'daily-mail', 'engadget', 'cnn', 'google-news', \
        'the-new-york-times', 'fox-news', 'bbc-news', 'the-verge']

app = Flask(__name__)

@app.route('/')
def index():
    companyNames = ['Microsoft', 'Walmart']
    for name in companyNames:
        sentimentClass(name, api_keys, sources)
    return render_template("index.html", content=content)

@app.route('/company/<companyName>')
def individualCompany(companyName):
    sentimentClass(companyName, api_keys, sources)
    return render_template("individual.html", content={"name": companyName})

# prevent cached responses
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
