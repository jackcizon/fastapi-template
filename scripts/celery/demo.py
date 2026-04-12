from typing import cast

from celery import Task
from celery.result import AsyncResult

from tasks.email.tasks import demo_task


def run_demo_task():
    res: AsyncResult = cast(Task, demo_task).delay()
    print(res.result)


if __name__ == "__main__":
    run_demo_task()
