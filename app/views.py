from django.http import HttpResponse
from django.shortcuts import render
from .tasks import send_mail_func
from .forms import NoticeBoardForm

# Create your views here.
def test(request):
    # send_mail_func.delay()
    # return HttpResponse("Sent!")
    form = NoticeBoardForm()
    return render(request, 'app/index.html', {'form': form})