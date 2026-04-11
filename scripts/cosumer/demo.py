from celery import Task

from tasks.email.tasks import send_verification_code


def aaa():
    send_verification_code.delay()


if __name__ == '__main__':
    aaa()