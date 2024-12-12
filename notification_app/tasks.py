import os
from django.core.mail import EmailMessage
from celery import shared_task


@shared_task(name='send_email_task')
def send_mail_task(subject, message, recepient_list):
    msg = EmailMessage(subject, message, os.environ.get("EMAIL_HOST_USER", 'waqasidrees15@gmail.com') , recepient_list)
    msg.content_subtype = 'html'
    msg.send()