from app import app
from flask import render_template, request, redirect, url_for

from webcrawler import crawl_and_save


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        error = None
        data = request.form['search'].split('|')
        if len(data) == 3:
            pass
    return render_template('index.html')
