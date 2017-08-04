from flask import Flask
from celery import Celery
from flask import jsonify, url_for, render_template
from scraping import LifehackerCountCommentsParser
from . import config

app = Flask(__name__)
# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config.from_object(config)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
def hello_world():
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



@celery.task(bind=True)
def scraping_lifehacker_task(self):
    parser = LifehackerCountCommentsParser()
    comment_counts = parser.run(update_state_func=self.update_state)
    return {
        'current': 100,
        'total': 100,
        'status': 'Task completed!',
        'result': comment_counts,
    }


if __name__ == '__main__':
    app.run()
