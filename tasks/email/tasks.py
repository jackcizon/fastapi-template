import smtplib
from email.mime.text import MIMEText

from src.core.config import settings
from tasks.main import app


@app.task
def demo_task() -> bool:
    return True


@app.task
def send_verification_code_email(to_email: str, verification_code: str, subject: str, content: str) -> bool:
    try:
        msg = MIMEText(f"{content}\nverification_code: {verification_code}\n")
        msg["Subject"] = subject
        msg["From"] = settings.smtp_from_email
        msg["To"] = to_email

        server = smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port)
        server.login(settings.smtp_from_email, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    finally:
        return False
