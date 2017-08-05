from celery import Celery
from app import app
from scraping import LifehackerCountCommentsParser

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


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
