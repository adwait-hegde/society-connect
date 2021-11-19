from django.http import HttpResponse
from django.shortcuts import render
from .tasks import send_mail_func


# Create your views here.
def test(request):
    # send_mail_func.delay()
    return HttpResponse("Sent!")