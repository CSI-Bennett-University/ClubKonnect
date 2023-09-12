from django.core.mail.backends.smtp import EmailBackend
from django.core.mail.backends.dummy import EmailBackend as DummyEmailBackend
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend
from anymail.backends.sendinblue import EmailBackend as SendinblueEmailBackend
import os
class ConditionalEmailBackend:
    def __init__(self, *args, **kwargs):
        # Check if the required environment variables are present
        email_host = os.environ.get("EMAIL_HOST")
        email_user = os.environ.get("EMAIL_HOST_USER")
        email_password = os.environ.get("EMAIL_HOST_PASSWORD")
        
        # Use SMTP backend if all environment variables are present
        if email_host and email_user and email_password:
            self.email_backend = EmailBackend(*args, **kwargs)
        else:
            # Use dummy backend if any of the environment variables is missing
            self.email_backend = ConsoleEmailBackend(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.email_backend, name)

    def send_messages(self, email_messages):
        try:
            return self.email_backend.send_messages(email_messages)
        except:
            self.email_backend = SendinblueEmailBackend()
            return self.email_backend.send_messages(email_messages)
