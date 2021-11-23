from django.contrib.auth import get_user_model

from celery import shared_task

# @shared_task(bind=True)
# def test_func(self):
#     #task
#     for i in range(10):
#         print("yesss ",i)
#     return "Done YAYYY!"

# from django.core import mail
#   MAIL SYSTEM START
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
#MAIL SYSTEM ENDS
# from django.utils.html import strip_tags

from django.core.mail import send_mail
from app.models import *
from societyconnect import settings
from django.utils import timezone
from datetime import timedelta


def send_mail(subject, html_template, user, context):
    subject = subject
    html_template = html_template
    to_email = user.email
    from_email=settings.DEFAULT_FROM_EMAIL
    html_message = render_to_string(html_template, context)
    message = EmailMessage(subject, html_message, from_email, [to_email])
    message.content_subtype = 'html' 
    message.send()


@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        # import html message.html file
        subject = "Society Connect Testing"
        html_template = 'app/mail_template.html'
        to_email = user.email
        from_email=settings.DEFAULT_FROM_EMAIL
        html_message = render_to_string(html_template, { 'user': user, })

        message = EmailMessage(subject, html_message, from_email, [to_email])
        message.content_subtype = 'html' # this is required because there is no plain text email message
        message.send()
        break
    return "Done"


@shared_task(bind=True)
def send_mail_bill(self):
    users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    for user in users:
        mail_subject = "Hi! Society Connect Testing"
        message = "If you are getting this mail, please text me on WhatsApp"
        to_email = user.email
        print('sending...')
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=False,
        )
    return "Done"

@shared_task(bind=True)
def send_mail_reminder(self):
    users = get_user_model().objects.all()
    for user in users:
        context = {'user':user}
        send_mail(subject="URGENT: Bill Payment Reminder!", html_template="app/mail_reminder.html",user=user, context=context)
    return "Done"

@shared_task(bind=True)
def send_mail_notice(self, pk):
    notice = NoticeBoard.objects.get(pk=pk)
    users = get_user_model().objects.all()
    for user in users:
        context = {'user':user, 'notice':notice}
        send_mail(subject="New Notice added to the Notice Board", html_template="app/mail_notice.html",user=user, context=context)
        break
    return "Done"


@shared_task(bind=True)
def send_mail_txn_status(self, tid, uid):
    txn = Transaction.objects.get(pk=tid)
    user = get_user_model().objects.get(pk=uid)
    context = {'user':user, 'txn':txn}
    if txn.status:
        send_mail(subject="Transaction Successful", html_template="app/mail_tsuccess.html",user=user, context=context)
    else:
        send_mail(subject="Transaction Failed", html_template="app/mail_tfail.html",user=user, context=context)
    return "Done"
