from celery import shared_task
import demo.mq.Receiver as rr

@shared_task
def startMq():
    print("1234")
    rr.start()

@shared_task
def add(x, y):
    return x + y