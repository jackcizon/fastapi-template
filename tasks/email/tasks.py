from tasks.main import app


@app.task
def demo_task():
    return True


@app.task
def send_verification_code():
    pass
