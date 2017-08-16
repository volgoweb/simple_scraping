from flask import jsonify, url_for, render_template, request
from app import app
from tasks import scraping_lifehacker_task


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/parse')
def scraping_page():
    return render_template('scraping.html')


@app.route('/run-scraping/', methods=['POST'])
def run_scruping():
    task = scraping_lifehacker_task.apply_async()
    data = {
        'Location': url_for('scraping_status', task_id=task.id),
    }
    return jsonify({}), 202, data


@app.route('/scraping-status/<task_id>', methods=['POST'])
def scraping_status(task_id):
    task = scraping_lifehacker_task.AsyncResult(task_id)
    data = {
        'state': task.state,
        'current': task.info.get('current') if isinstance(task.info, dict) else 0,
        'result': task.info.get('result') if isinstance(task.info, dict) else 0,
    }
    return jsonify(data)
