# http://stackoverflow.com/questions/20116573/in-celery-3-1-making-django-periodic-task
# http://127.0.0.1:9000/admin/djcelery/workerstate/
import datetime
import celery
from torrent import views


@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1))
def myfunc():
    print('periodic_task', 'myfunc')
    # views.collect_backgound()


from celery.task import periodic_task
from celery.schedules import crontab


@periodic_task(run_every=crontab(hour="*", minute="0", day_of_week="*"), ignore_result=True)
def my_test():
    print('periodic_task', 'my_test')


from celery import Celery
from celery.schedules import crontab

# app = Celery()
#
# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'add-every-monday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (16, 16),
#     },
#     'add-every-minute': {
#         'task': 'tasks.add',
#         'schedule': crontab(minute='*'),
#         'args': (1, 2),
#     }
# }


# @app.task
# def test(arg):
#     print(arg)

# from celery import task
#
# @task
# def add(x, y):
#     print(x, y, x+y)


# from celery import task
#
# @task()
# def add(x, y):
#     return x + y