from app import app
from flask import render_template, request, redirect, url_for

from .webcrawler.models.query_model import QueryModel
from .webcrawler.models import storage
from .webcrawler.crawler import ContentFetcher


def get_post_data():
    values = request.form.get('search').split('|')
    keys = ['king', 'head', 'body']
    data = {k: v for k, v in zip(keys, values)}
    print(data)
    return redirect(url_for('result', **data))


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        return get_post_data()
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        return get_post_data()
    query = QueryModel(**request.args)
    storage.new(query)
    storage.save()

    fetcher = ContentFetcher(**request.args)
    results = fetcher.process()
    if results:
        return render_template('result.html', results=results())
    return render_template('result.html')
