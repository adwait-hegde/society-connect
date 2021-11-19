from django.contrib.auth import get_user_model

from celery import shared_task

# @shared_task(bind=True)
# def test_func(self):
#     #task
#     for i in range(10):
#         print("yesss ",i)
#     return "Done YAYYY!"


from django.core.mail import send_mail
from societyconnect import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
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